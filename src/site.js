(function(){
  // Rack illustration on the home page: which ports are lit, carry PoE, or blink with traffic
  var PORTS={
    core:[[0,1,2,3,4,5,6,8,9,12,13,14,15,16,18,20,21,23],[3,4,5,14,15],[1,6,13,20]],
    patch:[[0,1,2,3,4,5,6,8,9,12,13,14,15,16,18,20,21,23],[],[]],
    access:[[0,1,2,3,4,5,6,7,10,11,12,17,19,22],[0,1,2,3,4,5,6,7],[2,11,19]]
  };
  document.querySelectorAll('[data-ports]').forEach(function(el){
    var cfg=PORTS[el.getAttribute('data-ports')]; if(!cfg) return;
    for(var i=0;i<24;i++){
      var p=document.createElement('span'); p.className='port';
      if(cfg[0].indexOf(i)>-1) p.classList.add('on');
      if(cfg[1].indexOf(i)>-1) p.classList.add('poe');
      if(cfg[2].indexOf(i)>-1) p.classList.add('blink');
      p.appendChild(document.createElement('i')); el.appendChild(p);
    }
  });

  var btn=document.getElementById('menu-btn'), links=document.getElementById('nav-links');
  if(btn&&links){
    btn.addEventListener('click',function(){
      var open=links.hidden; links.hidden=!open; btn.setAttribute('aria-expanded',String(open)); btn.textContent=open?'Close':'Menu';
    });
  }

  var yr=document.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();

  var form=document.getElementById('quote-form'), status=document.getElementById('form-status');
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var name=form.name.value.trim(), co=form.company.value.trim(), em=form.email.value.trim();
      if(!name||!co||!em){status.textContent='Please add your name, business name, and email.';return;}
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){status.textContent='Please check your email address.';return;}
      var btn=form.querySelector('button[type=submit]'); btn.disabled=true; status.textContent='Sending...';
      fetch('https://formsubmit.co/ajax/'+['connect','kickstarttechsolutions.com'].join('@'),{method:'POST',headers:{'Accept':'application/json'},body:new FormData(form)})
        .then(function(r){return r.json().then(function(d){if(!r.ok||String(d.success)!=='true')throw 0;});})
        .then(function(){status.textContent='Thanks, '+name.split(' ')[0]+'. We will be in touch within one business day.';form.reset();})
        .catch(function(){status.textContent='Sorry, that did not send. Please email connect@kickstarttechsolutions.com or call +1 (770) 289-5440.';})
        .then(function(){btn.disabled=false;});
    });
  }
})();
