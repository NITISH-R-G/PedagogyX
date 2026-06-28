export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between shadow-sm">
      <h1 className="text-xl font-bold text-gray-900">PedagogyX Admin</h1>
      <nav className="flex space-x-6 text-sm font-medium text-gray-600">
        <a
          href="#"
          className="text-blue-600 font-semibold border-b-2 border-blue-600 pb-1"
        >
          Dashboard
        </a>
        <a href="#" className="hover:text-gray-900 transition-colors">
          Teachers
        </a>
        <a href="#" className="hover:text-gray-900 transition-colors">
          Recordings
        </a>
        <a href="#" className="hover:text-gray-900 transition-colors">
          Analytics
        </a>
        <a href="#" className="hover:text-gray-900 transition-colors">
          Settings
        </a>
      </nav>
    </header>
  );
}
