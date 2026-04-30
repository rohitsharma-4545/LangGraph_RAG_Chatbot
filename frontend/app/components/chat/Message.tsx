import { ChatMessage } from "@/types/chat";
import clsx from "clsx";

export default function Message({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  console.log(message);

  return (
    <div className={clsx("flex gap-3", isUser && "justify-end")}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs text-black">
          AI
        </div>
      )}

      <div
        className={clsx(
          "px-4 py-3 rounded-2xl max-w-[75%] text-sm leading-relaxed shadow-sm",
          isUser
            ? "bg-blue-600 text-white rounded-br-sm"
            : "bg-gray-100 text-gray-900 border rounded-bl-sm",
        )}
      >
        {message.content === "..." ? (
          <span className="animate-pulse text-gray-400">Thinking...</span>
        ) : (
          message.content
        )}
      </div>
    </div>
  );
}
