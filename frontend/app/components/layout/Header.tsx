"use client";

export default function Header({
  onAdminClick,
  isAdmin,
  onLogout,
}: {
  onAdminClick: () => void;
  isAdmin: boolean;
  onLogout: () => void;
}) {
  return (
    <div className="h-14 border-b flex items-center justify-between px-6 bg-white">
      <h1 className="font-semibold">AI Assistant</h1>

      <div className="flex items-center gap-3">
        {!isAdmin ? (
          <button
            onClick={onAdminClick}
            className="text-sm text-gray-500 hover:text-black"
          >
            Admin
          </button>
        ) : (
          <button onClick={onLogout} className="text-sm text-red-500">
            Logout Admin
          </button>
        )}
      </div>
    </div>
  );
}
