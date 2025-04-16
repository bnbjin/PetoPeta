import { useThreadRuntime } from "@assistant-ui/react";
import { Card, CardTitle } from "./ui/card";

const suggestedQuestions = [
  "I have a corgi of 4 years old named Mango, 17kg of weight, female. Help me make a healthy and nutritional diet plan for her so to lose the weight.",
  "Can a cat eat watermelon?",
  "What is the best weight for a husky of 5 years old?",
  "What can you do?",
];

export function SuggestedQuestions() {
  const threadRuntime = useThreadRuntime();

  const handleSend = (text: string) => {
    threadRuntime.append({
      role: "user",
      content: [{ type: "text", text }],
    });
  };

  return (
    <div className="w-full grid grid-cols-1 sm:grid-cols-2 gap-4">
      {suggestedQuestions.map((question, idx) => (
        <Card
          onClick={() => handleSend(question)}
          key={`suggested-question-${idx}`}
          className="w-full bg-[#282828] border-gray-600 cursor-pointer transition-colors ease-in hover:bg-[#2b2b2b]"
        >
          <CardTitle className="p-4 text-gray-200 font-normal text-sm">
            {question}
          </CardTitle>
        </Card>
      ))}
    </div>
  );
}
