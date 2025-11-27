export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#1a1a1a] text-white flex items-center justify-center">
      <div className="flex flex-col md:flex-row gap-10 items-center">
        {/* Speedometer Box */}
        <div className="bg-gray-800 w-72 h-72 rounded-xl shadow-xl flex flex-col items-center justify-start relative">
          {/* Semicircle border */}
          <div className="w-48 h-24 border-t-4 border-white rounded-t-full absolute top-4"></div>

          {/* Needle resting flat */}
          <div className="h-1 w-24 bg-red-500 absolute left-[calc(50%-12px)] top-24 origin-left rotate-0"></div>


          <p className="absolute bottom-6 text-3xl text-gray-300">Speedometer</p>
        </div>

        {/* Center Number Box */}
        <div className="bg-gray-800 w-32 h-32 p-4 rounded-xl shadow-xl flex flex-col items-center justify-center">
          <h2 className="text-3xl font-bold">42</h2>
          <p className="text-gray-400 text-sm">Current Value</p>
        </div>

        {/* Power Meter Box */}
        <div className="bg-gray-800 w-72 h-72 p-6 rounded-xl shadow-xl flex items-center justify-center">
          <p className="text-3xl text-gray-300">Power Meter</p>
        </div>
      </div>
    </div>
  );
}
