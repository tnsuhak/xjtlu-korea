document.addEventListener('click',function(e){
  const btn=e.target.closest('.youtube-lite[data-youtube-id]');
  if(!btn||btn.dataset.loaded==='true') return;
  const id=btn.dataset.youtubeId;
  if(!id) return;
  const iframe=document.createElement('iframe');
  iframe.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0';
  iframe.title=btn.dataset.videoTitle||'XJTLU 공식 YouTube 영상';
  iframe.loading='lazy';
  iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
  iframe.allowFullscreen=true;
  btn.dataset.loaded='true';
  btn.replaceChildren(iframe);
});
