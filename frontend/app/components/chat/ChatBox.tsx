import { ChatMessage } from "@/types/chat";
import Message from "./Message";
import { RefObject } from "react";

export default function ChatBox({
  messages,
  bottomRef,
  loading,
}: {
  messages: ChatMessage[];
  bottomRef: RefObject<HTMLDivElement | null>;
  loading: boolean;
}) {
  return (
    <div className="flex-1 overflow-y-auto px-6 py-10">
      <div className="max-w-3xl mx-auto space-y-6">
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs text-black">
              AI
            </div>

            <div className="px-4 py-3 rounded-2xl bg-gray-100 text-gray-900 text-sm animate-pulse">
              Thinking...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
