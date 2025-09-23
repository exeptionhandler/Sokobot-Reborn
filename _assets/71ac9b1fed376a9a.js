(self["webpackChunk_canva_web"] = self["webpackChunk_canva_web"] || []).push([[21988],{

/***/ 980813:
function(_, __, __webpack_require__) {__webpack_require__.n_x = __webpack_require__.n;const __web_req__ = __webpack_require__;__web_req__(905716);self._5f74ec40302898c5a55451c9fbd04240 = self._5f74ec40302898c5a55451c9fbd04240 || {};(function(__c) {var ajc=__webpack_require__(186901).EW;__c.K2=class{static D(a){__c.M(a,{lv:ajc,gT:ajc,step:ajc})}get kind(){return"band"}clone({dc:a=this.dc,xc:b=this.xc,bh:c=this.bh,Pd:d=this.Pd}){return new __c.K2({dc:a,xc:b,bh:c,Pd:d})}get(a){const b=this.dc().indexOf(a);__c.u(b!==-1,`value ${a} must exist in domain`);const [c,d]=this.xc();return c+b*this.step*Math.sign(d-c)}get lv(){const [a,b]=this.xc(),c=Math.abs(b-a),d=this.dc();if(d.length<=1)return c;const e=this.bh(),f=(1-e)*d.length;return f/(f+e*(d.length-1))*c/d.length}get gT(){const a=
this.dc();if(a.length<=1)return 0;const [b,c]=this.xc(),d=this.bh(),e=d*(a.length-1);return e/((1-d)*a.length+e)*Math.abs(c-b)/(a.length-1)}get step(){return this.lv+this.gT}Rea(a,b,c){__c.u(a.index!==b.index);var d=this.bh(),e=b.index-a.index,f=b.index-a.index;const g=(1-d)*e;d*=f;e=g/(g+d)*(b.center-a.center)/e;f=e+d/(g+d)*(b.center-a.center)/f;return[a.center-e/2-f*a.index,b.center+e/2+f*(c-b.index-1)]}Qea(a,b,c){const d=this.bh();var e=.5+a.index;const f=(1-d)*e;e=f/(f+d*a.index)*(a.center-b)/
e;return[b,a.center+e/2+(e+e/(1-d)*d)*(c-a.index-1)]}Pea(a,b,c){const d=this.bh(),e=.5+c-a.index-1,f=(1-d)*e;c=f/(f+d*(c-a.index-1))*(b-a.center)/e;return[a.center-c/2-(c+c/(1-d)*d)*a.index,b]}constructor({dc:a,xc:b,bh:c,Pd:d}){__c.K2.D(this);this.dc=a;this.xc=b;this.bh=c;this.Pd=d}};
}).call(self, self._5f74ec40302898c5a55451c9fbd04240);}

}])
//# sourceMappingURL=sourcemaps/71ac9b1fed376a9a.js.map