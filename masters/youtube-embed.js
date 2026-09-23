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
