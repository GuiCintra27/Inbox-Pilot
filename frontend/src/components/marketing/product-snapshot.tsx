export function ProductSnapshot() {
  return (
    <div className="relative aspect-[700/410] w-full max-w-[320px] min-w-0 sm:max-w-[420px] lg:max-w-[560px] xl:max-w-[900px]">
      <div className="absolute left-[8.4%] top-[9%] h-[73%] w-[69%] rounded-[20px] bg-white shadow-[0_40px_100px_-38px_rgba(15,23,42,0.28)]">
        <div className="flex h-[14.2%] items-center rounded-t-[20px] border-b border-[#f0ede9] bg-[#fdfcfa] px-[5.4%]">
          <span className="h-[8px] w-[8px] rounded-full bg-[#f6c2c0]" />
          <span className="mx-auto pr-4 text-[10px] font-medium tracking-[0.01em] text-slate-500">
            inbox-pilot-demo.v2
          </span>
        </div>

        <div className="px-[5.4%] pt-[5.4%]">
          <div className="h-[8px] w-[50%] rounded-full bg-[#f2efea]" />
          <div className="mt-[4.5%] h-[8px] w-[44%] rounded-full bg-[#f5f2ee]" />

          <div className="mt-[11.4%] flex items-center justify-between text-[10px] font-medium text-slate-700">
            <span>Produtivo</span>
            <span>Confiança: 98%</span>
            <span className="h-[20px] w-[20px] rounded-full bg-[#c7f5ff]" />
          </div>

          <div className="mt-[5%] rounded-[11px] bg-[#06081c] px-[5.4%] py-[4.2%]">
            <div className="h-[7px] w-full rounded-full bg-[#24273f]" />
            <div className="mt-[4.2%] h-[7px] w-[86%] rounded-full bg-[#20243c]" />
          </div>
        </div>
      </div>

      <div className="absolute right-[0.8%] top-[19%] h-[36%] w-[22%] rounded-full bg-[radial-gradient(circle,rgba(255,255,255,0.88)_0%,rgba(255,255,255,0)_70%)] blur-2xl" />
    </div>
  );
}
