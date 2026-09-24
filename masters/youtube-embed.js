document.addEventListener('error',function(e){
  const img=e.target.closest?.('.youtube-lite img[data-fallback]');
  if(!img||img.dataset.fallbackUsed==='true') return;
  img.dataset.fallbackUsed='true';
  img.src=img.dataset.fallback;
},true);

document.addEventListener('click',function(e){
  const btn=e.target.closest('.youtube-lite[data-youtube-id]');
  if(!btn||btn.dataset.loaded==='true') return;
  const id=btn.dataset.youtubeId;
  if(!id) return;
  const iframe=document.createElement('iframe');
  iframe.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0';
  iframe.title=btn.dataset.videoTitle||'XJTLU 공식 YouTube 영상';
  iframe.loading='lazy';
  iframe.referrerPolicy='strict-origin-when-cross-origin';
  iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
  iframe.allowFullscreen=true;
  btn.dataset.loaded='true';
  btn.replaceChildren(iframe);
});

function normalizeMastersNavigation(){
  const labels={
    '/masters/':'석사 홈',
    '/masters/programmes.html':'54개 석사 전공',
    '/masters/admission-requirements-2027.html':'2027 입학조건',
    '/masters/tuition-scholarships-2027.html':'2027 학비·장학금',
    '/masters/#mres':'MRes 연구석사'
  };

  document.querySelectorAll('.navlinks a,.mobile-nav a').forEach(function(a){
    const href=a.getAttribute('href');
    if(labels[href]) a.textContent=labels[href];
    if(href==='/'){
      a.textContent='XJTLU Korea 메인으로 →';
      a.classList.add('main-site');
      a.setAttribute('aria-label','XJTLU Korea 전체 사이트 메인으로 이동');
    }
  });

  document.querySelectorAll('.navlinks,.mobile-nav').forEach(function(nav){
    if(!nav.querySelector('a[href="/masters/#mres"]')){
      const mres=document.createElement('a');
      mres.href='/masters/#mres';
      mres.textContent='MRes 연구석사';
      const main=nav.querySelector('a[href="/"]');
      const consult=nav.querySelector('.consult');
      nav.insertBefore(mres,main||consult||null);
    }
  });
}
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',normalizeMastersNavigation);
}else{
  normalizeMastersNavigation();
}

