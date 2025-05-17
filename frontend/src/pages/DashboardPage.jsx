import useAuthStore from '../store/authStore';

export default function DashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">歡迎回來</h1>
        <div className="space-y-4">
          <p className="text-gray-600">
            您好，{user?.username || user?.email}！歡迎使用使用者管理系統。
          </p>
          <div className="border-t border-gray-200 pt-4">
            <h2 className="text-lg font-medium text-gray-900 mb-2">快速連結</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <a
                href="/users"
                className="block p-4 rounded-lg border border-gray-200 hover:border-indigo-500 hover:shadow-md transition-all"
              >
                <h3 className="text-lg font-medium text-gray-900">使用者管理</h3>
                <p className="text-gray-500 mt-1">管理系統使用者，包括新增、編輯和刪除。</p>
              </a>
              {user?.is_admin && (
                <div className="block p-4 rounded-lg border border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">系統設定</h3>
                  <p className="text-gray-500 mt-1">即將推出：系統設定和進階功能。</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 