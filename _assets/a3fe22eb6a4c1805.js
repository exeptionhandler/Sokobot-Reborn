(self["webpackChunk_canva_web"] = self["webpackChunk_canva_web"] || []).push([[97668],{

/***/ 302749:
function(_, __, __webpack_require__) {__webpack_require__.n_x = __webpack_require__.n;const __web_req__ = __webpack_require__;__web_req__(905716);self._5f74ec40302898c5a55451c9fbd04240 = self._5f74ec40302898c5a55451c9fbd04240 || {};(function(__c) {var aic=__webpack_require__(186901).EW;__c.A2=class{static D(a){__c.M(a,{step:aic})}get kind(){return"point"}clone({dc:a=this.dc,xc:b=this.xc,bh:c=this.bh,Pd:d=this.Pd,inverse:e=this.inverse}){return new __c.A2({dc:a,xc:b,bh:c,Pd:d,inverse:e})}snapshot(){const a=this.dc(),b=this.xc();return new __c.A2({dc:()=>a,xc:()=>b,bh:this.bh,Pd:this.Pd,inverse:this.inverse})}get(a){const b=this.dc();var c=b.indexOf(a);c=this.inverse?b.length-1-c:c;__c.u(c!==-1,`value ${a} must exist in domain`);const [d,e]=this.xc();a=b.length===1?.5:this.bh();return d+
(a*this.step+c*this.step)*Math.sign(e-d)}get step(){const a=this.dc().length+2*this.bh(),[b,c]=this.xc();return Math.abs(c-b)/Math.max(a-1,1)}Rea(a,b,c){__c.u(a.index!==b.index);const d=this.bh(),e=(b.center-a.center)/(b.index-a.index);return[a.center-(d+a.index)*e,b.center+(d+c-b.index-1)*e]}Qea(a,b,c){const d=this.bh();return[b,a.center+(a.center-b)/(a.index+d)*(d+c-a.index-1)]}Pea(a,b,c){const d=this.bh();return[a.center-(b-a.center)/(c-a.index-1+d)*(d+a.index),b]}constructor({dc:a,xc:b,bh:c,Pd:d,
inverse:e=!1}){__c.A2.D(this);this.dc=a;this.xc=b;this.bh=c;this.Pd=d;this.inverse=e}};
}).call(self, self._5f74ec40302898c5a55451c9fbd04240);}

}])
//# sourceMappingURL=sourcemaps/a3fe22eb6a4c1805.js.map