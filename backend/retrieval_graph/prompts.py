from langsmith import Client
from backend.prompts_local.en import *

"""Default prompts."""

client = Client()
# fetch from langsmith
# ROUTER_SYSTEM_PROMPT = (
#     client.pull_prompt("langchain-ai/chat-langchain-router-prompt")
#     .messages[0]
#     .prompt.template
# )
ROUTER_SYSTEM_PROMPT = ROUTER_SYSTEM_PROMPT_STR

# GENERATE_QUERIES_SYSTEM_PROMPT = (
#     client.pull_prompt("langchain-ai/chat-langchain-generate-queries-prompt")
#     .messages[0]
#     .prompt.template
# )
GENERATE_QUERIES_SYSTEM_PROMPT = GENERATE_QUERIES_SYSTEM_PROMPT_STR

# MORE_INFO_SYSTEM_PROMPT = (
#     client.pull_prompt("langchain-ai/chat-langchain-more-info-prompt")
#     .messages[0]
#     .prompt.template
# )
MORE_INFO_SYSTEM_PROMPT = MORE_INFO_SYSTEM_PROMPT_STR

# RESEARCH_PLAN_SYSTEM_PROMPT = (
#     client.pull_prompt("langchain-ai/chat-langchain-research-plan-prompt")
#     .messages[0]
#     .prompt.template
# )
RESEARCH_PLAN_SYSTEM_PROMPT = RESEARCH_PLAN_SYSTEM_PROMPT_STR

# GENERAL_SYSTEM_PROMPT = (
#     client.pull_prompt("langchain-ai/chat-langchain-general-prompt")
#     .messages[0]
#     .prompt.template
# )
GENERAL_SYSTEM_PROMPT = GENERAL_SYSTEM_PROMPT_STR

# RESPONSE_SYSTEM_PROMPT = (
#     client.pull_prompt("langchain-ai/chat-langchain-response-prompt")
#     .messages[0]
#     .prompt.template
# )
RESPONSE_SYSTEM_PROMPT = RESPONSE_SYSTEM_PROMPT_STR
