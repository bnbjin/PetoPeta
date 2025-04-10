from typing import List, Dict, Annotated, cast
from dataclasses import dataclass, field
from langchain_core.runnables import RunnableConfig
from langgraph.config import get_store
from langgraph.graph import StateGraph, START, END
from langgraph.store.base import BaseStore
from langgraph.prebuilt import InjectedStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, AIMessage

from backend.retrieval_graph.configuration import AgentConfiguration
from backend.retrieval_graph.state import InputState, Pet, PetList
from backend.retrieval_graph.pet_manager.tools import get_pets, add_or_update_pet
from backend.utils import load_chat_model
from backend.prompts_local.en import (
    FILTER_PETS_RECORDED_SYSTEM_PROMPT_STR,
    FILTER_PETS_RECORDED_AI_PROMPT_STR,
    FILTER_PETS_NOT_RECORDED_SYSTEM_PROMPT_STR,
)


@dataclass(kw_only=True)
class PetInformationFilterState(InputState):
    """State of the pet information filter graph."""

    pets_recorded: List[Dict] = field(default_factory=list)

    target_pets_recorded: List[Dict] = field(default_factory=list)

    new_pets_valid: List[Pet] = field(default_factory=list)

    new_pets_invalid: List[Pet] = field(default_factory=list)


async def get_all_recorded_pets(
    state: PetInformationFilterState,
    *,
    config: RunnableConfig,
) -> Dict[str, List[Dict]]:
    pets = await get_pets.ainvoke({}, config=config)

    return {"pets_recorded": pets}


async def filter_pets_recorded(
    state: PetInformationFilterState,
    *,
    config: RunnableConfig,
) -> Dict[str, List[Dict]]:
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)

    pets = state.pets_recorded

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=FILTER_PETS_RECORDED_SYSTEM_PROMPT_STR),
            AIMessage(
                content=FILTER_PETS_RECORDED_AI_PROMPT_STR.format(pets_recorded=pets)
            ),
            *state.messages,
        ]
    )

    messages = prompt.format_messages()
    response = await model.with_structured_output(PetList).ainvoke(messages)
    response = cast(PetList, response)

    return {"target_pets_recorded": response.pets}


async def filter_pets_not_recorded(
    state: PetInformationFilterState,
    *,
    config: RunnableConfig,
) -> Dict[str, List[Dict]]:
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)

    pets = state.pets_recorded

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=FILTER_PETS_NOT_RECORDED_SYSTEM_PROMPT_STR),
            AIMessage(
                content=FILTER_PETS_RECORDED_AI_PROMPT_STR.format(pets_recorded=pets)
            ),
            *state.messages,
        ]
    )

    messages = prompt.format_messages()
    response = await model.with_structured_output(PetList).ainvoke(messages)
    response = cast(PetList, response)

    return {"new_pets_invalid": response.pets}


async def add_new_pets_to_storage(
    state: PetInformationFilterState,
    *,
    config: RunnableConfig,
) -> Dict:
    for pet in state.new_pets_invalid:
        is_valid = []
        for must_have_key in ["name", "species"]:
            is_valid.append(pet.get(must_have_key, "") != "")
        if all(is_valid):
            await add_or_update_pet.ainvoke(dict(pet), config=config)
    return {}


builder = StateGraph(PetInformationFilterState)

builder.add_node(get_all_recorded_pets)
builder.add_node(filter_pets_recorded)
builder.add_node(filter_pets_not_recorded)
builder.add_node(add_new_pets_to_storage)
builder.add_edge(START, "get_all_recorded_pets")
builder.add_edge("get_all_recorded_pets", "filter_pets_recorded")
builder.add_edge("filter_pets_recorded", "filter_pets_not_recorded")
builder.add_edge("filter_pets_not_recorded", "add_new_pets_to_storage")
builder.add_edge("add_new_pets_to_storage", END)

graph = builder.compile()
graph.name = "PetInformationFilterGraph"
