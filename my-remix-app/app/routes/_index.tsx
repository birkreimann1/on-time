export default function Index() {
  return (
    <div className="flex flex-col h-screen items-center justify-center">
      <div className="flex flex-col gap-4 bg-black w-full p-6">
        <div className="w-full bg-neutral-800 p-4 rounded-full text-neutral-400">Start</div>
        <div className="w-full bg-neutral-800 p-4 rounded-full text-neutral-400">Ziel</div>
      </div>
      <div className="flex flex-grow justify-center items-center bg-green-700 w-full">Map</div>
    </div>
  );
}
