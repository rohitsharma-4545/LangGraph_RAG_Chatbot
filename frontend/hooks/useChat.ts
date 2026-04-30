"use client";

import { useState } from "react";
import { ChatMessage } from "@/types/chat";
import { v4 as uuidv4 } from "uuid";

export function useChat(token: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (query: string) => {
    if (!query.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: uuidv4(),
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: JSON.stringify({ query }),
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      let assistantMessage = "";
      const assistantId = uuidv4();

      setMessages((prev) => [
        ...prev,
        { id: assistantId, role: "assistant", content: "..." },
      ]);

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);

        for (let line of chunk.split("\n")) {
          if (line.startsWith("data: ")) {
            const text = line.replace("data: ", "");

            if (text.startsWith("ERROR:")) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId
                    ? {
                        ...m,
                        content:
                          text.replace("ERROR:", "").trim() ||
                          "Something went wrong",
                      }
                    : m,
                ),
              );

              setLoading(false);
              return;
            }
            if (text === "[DONE]") break;

            assistantMessage += text;

            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId ? { ...m, content: assistantMessage } : m,
              ),
            );
          }
        }
      }
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, sendMessage, setMessages };
}
