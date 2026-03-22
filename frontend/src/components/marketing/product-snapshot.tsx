export function ProductSnapshot() {
  return (
    <div className="relative h-[340px] w-[560px]">
      <div className="absolute left-[54px] top-[34px] h-[240px] w-[360px] rounded-[18px] bg-white shadow-[0_35px_90px_-34px_rgba(15,23,42,0.32)]">
        <div className="flex h-[34px] items-center rounded-t-[18px] border-b border-[#f0ede9] bg-[#fdfcfa] px-5">
          <span className="h-[8px] w-[8px] rounded-full bg-[#f6c2c0]" />
          <span className="mx-auto pr-4 text-[10px] font-medium tracking-[0.01em] text-slate-500">
            inbox-pilot-demo.v2
          </span>
        </div>

        <div className="px-5 pt-5">
          <div className="h-[8px] w-[180px] rounded-full bg-[#f2efea]" />
          <div className="mt-4 h-[8px] w-[160px] rounded-full bg-[#f5f2ee]" />

          <div className="mt-9 flex items-center justify-between text-[10px] font-medium text-slate-700">
            <span>Produtivo</span>
            <span>Confiança: 98%</span>
            <span className="h-[20px] w-[20px] rounded-full bg-[#c7f5ff]" />
          </div>

          <div className="mt-4 rounded-[10px] bg-[#06081c] px-5 py-4">
            <div className="h-[7px] w-full rounded-full bg-[#24273f]" />
            <div className="mt-3 h-[7px] w-[86%] rounded-full bg-[#20243c]" />
          </div>
        </div>
      </div>

      <div className="absolute right-[8px] top-[74px] h-[110px] w-[110px] rounded-full bg-[radial-gradient(circle,rgba(255,255,255,0.92)_0%,rgba(255,255,255,0)_70%)] blur-2xl" />
    </div>
  );
}
