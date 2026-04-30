"use client";

import { useRef, useLayoutEffect, useState, useEffect } from "react";
import ChatBox from "./components/chat/ChatBox";
import InputBox from "./components/chat/InputBox";
import Header from "./components/layout/Header";
import AdminPanel from "./components/admin/AdminPanel";
import AdminLoginModal from "./components/admin/AdminLoginModal";
import { useAdmin } from "@/hooks/useAdmin";
import { useChat } from "@/hooks/useChat";

export default function Home() {
  const { isAdmin, token, login, logout } = useAdmin();
  const { messages, loading, sendMessage } = useChat(token);

  const [showModal, setShowModal] = useState(false);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useLayoutEffect(() => {
    bottomRef.current?.scrollIntoView();
  }, [messages]);

  useEffect(() => {
    if (!token) {
      login("", "user");
    }
  }, [token, login]);

  return (
    <div className="h-screen flex">
      {isAdmin && <AdminPanel token={token} />}

      <div className="flex-1 flex flex-col">
        <Header
          isAdmin={isAdmin}
          onAdminClick={() => setShowModal(true)}
          onLogout={logout}
        />

        <ChatBox messages={messages} bottomRef={bottomRef} loading={loading} />

        <InputBox onSend={sendMessage} loading={loading} />
      </div>

      {showModal && (
        <AdminLoginModal
          onClose={() => setShowModal(false)}
          onLogin={(password) => login(password, "admin")}
        />
      )}
    </div>
  );
}
