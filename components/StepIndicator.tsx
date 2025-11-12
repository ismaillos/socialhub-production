
export default function StepIndicator({ current }: { current:1|2|3 }){
  const steps = ["Describe","Generate","Publish"];
  return (
    <div className="flex flex-wrap items-center gap-3 mb-6">
      {steps.map((label, idx)=>{
        const id = idx+1; const active = id===current; const done = id<current;
        return (
          <div className="flex items-center gap-2" key={id}>
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold border
              ${done? "bg-vl_primary text-white border-vl_primary" : active? "bg-vl_accent text-white border-vl_accent" : "bg-white text-slate-400 border-slate-300"}`}>
              {id}
            </div>
            <span className={`${active||done? "text-slate-900 font-medium":"text-slate-400"}`}>{label}</span>
            {id!==3 && <div className="hidden sm:block w-8 h-px bg-slate-300" />}
          </div>
        );
      })}
    </div>
  );
}
