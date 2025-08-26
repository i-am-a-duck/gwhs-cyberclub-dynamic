console.log('GWHS Cybersecurity Club dynamic site loaded');

// GWHS Cybersecurity Club dynamic site loaded

(function(){
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // IntersectionObserver: add .in to .reveal
  if ('IntersectionObserver' in window){
    const io = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        if(e.isIntersecting){
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
  } else {
    // fallback
    document.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'));
  }

  // Subtle parallax on hero grid
  if(!prefersReduced){
    const grid = document.querySelector('.hero-grid');
    if(grid){
      window.addEventListener('mousemove', (e)=>{
        const x = (e.clientX / window.innerWidth - 0.5) * 6;
        const y = (e.clientY / window.innerHeight - 0.5) * 6;
        grid.style.transform = `translate(${x}px, ${y}px)`;
      }, { passive: true });
    }
  }
})();

// === Hero 右上角动词轮换 ===
(function(){
  const el = document.getElementById('verbRotator');
  if(!el) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // 想用你原来的词，把下面替换成 ["create","protect","defense","attack","destory"]
  const words = ["Create","Defend","Attack","Destroy","Protect"];

  let i = 0;
  const change = ()=>{
    i = (i + 1) % words.length;

    // 动画：先标记闪烁与遮挡
    if(!prefersReduced){
      el.classList.add('flash','glitch');
      // 稍等一小会换词，制造“遮挡 → 变换 → 发光”的感觉
      setTimeout(()=>{ el.textContent = words[i]; }, 160);
      // 结束后清理 class
      setTimeout(()=>{ el.classList.remove('glitch'); }, 480);
      setTimeout(()=>{ el.classList.remove('flash'); }, 820);
    }else{
      el.textContent = words[i];
    }
  };

  // 初始 1.6s 后开始，每 1.8s 轮换一次
  setTimeout(change, 1600);
  setInterval(change, 1800);
})();
