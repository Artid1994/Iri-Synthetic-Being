/* Brain Atlas Obsidian plugin */
var Ue=Object.defineProperty;var lo=Object.getOwnPropertyDescriptor;var co=Object.getOwnPropertyNames;var uo=Object.prototype.hasOwnProperty;var fo=(t,r)=>{for(var e in r)Ue(t,e,{get:r[e],enumerable:!0})},po=(t,r,e,o)=>{if(r&&typeof r=="object"||typeof r=="function")for(let i of co(r))!uo.call(t,i)&&i!==e&&Ue(t,i,{get:()=>r[i],enumerable:!(o=lo(r,i))||o.enumerable});return t};var ho=t=>po(Ue({},"__esModule",{value:!0}),t);var Sr={};fo(Sr,{default:()=>Fe});module.exports=ho(Sr);var Te=require("obsidian");var se=["person","project","concept","decision","question","tool","workThread","dailyNote","source","repo","incident","organization","index","unknown"];var k=["frontal","parietal","temporal","occipital","cerebellum","stem"];function pe(){return{frontal:!0,parietal:!0,temporal:!0,occipital:!0,cerebellum:!0,stem:!0}}function Le(t){return{...pe(),...t!=null?t:{}}}function Ce(t,r,e){return{...Le(t),[r]:e}}function st(t){return Object.fromEntries(k.map(r=>[r,t]))}function Z(t,r,e){return(t?Le(r)[t]:!0)?e?t===e?1:.16:1:.08}var mo=["graphite","ink","magma","bio","acid","aurora","daylight"],bo=["smooth","balanced","batterySaver","mobile"],go=["auto","webgl2","canvas2d"],F={palette:"graphite",performancePreset:"smooth",frontmatterKindKeys:["kind","type","category"],frontmatterKindValueMap:{},frontmatterRegionKeys:["brain_region","brainRegion","lobe","region"],tagKindMap:{project:"project",person:"person",decision:"decision",question:"question",tool:"tool",concept:"concept",source:"source",daily:"dailyNote",moc:"concept",thread:"workThread",index:"index"},folderKindMap:{People:"person",Projects:"project",Sources:"source",Daily:"dailyNote",Journal:"dailyNote",Concepts:"concept",Topics:"concept",MOCs:"concept",Maps:"concept",Index:"index",Home:"index"},frontmatterRegionValueMap:{},tagRegionMap:{},folderRegionMap:{},noteRegionMap:{},treatDateFilesAsDaily:!0,honorDailyNotesFormat:!0,dailyNoteDateFormat:"YYYY-MM-DD",nodeCap:1500,edgeCap:4e3,idleAutoRotate:!0,showLobeLabels:!0,showLegendChip:!0,enabledLobes:pe(),clickAction:"current",hubThresholdPercent:4,pinnedNodePositions:{},defaultKind:"concept",inferKindsFromLinks:!0,rendererMode:"auto"};function We(t){var r,e,o,i,n,a,c;return{...F,...t!=null?t:{},frontmatterKindKeys:(r=t==null?void 0:t.frontmatterKindKeys)!=null?r:F.frontmatterKindKeys,frontmatterRegionKeys:(e=t==null?void 0:t.frontmatterRegionKeys)!=null?e:F.frontmatterRegionKeys,frontmatterKindValueMap:Co(t==null?void 0:t.frontmatterKindValueMap,F.frontmatterKindValueMap),tagKindMap:lt(t==null?void 0:t.tagKindMap,F.tagKindMap,!0),folderKindMap:lt(t==null?void 0:t.folderKindMap,F.folderKindMap,!1),frontmatterRegionValueMap:Po(t==null?void 0:t.frontmatterRegionValueMap,F.frontmatterRegionValueMap),tagRegionMap:je(t==null?void 0:t.tagRegionMap,F.tagRegionMap,!0),folderRegionMap:je(t==null?void 0:t.folderRegionMap,F.folderRegionMap,!1),noteRegionMap:je(t==null?void 0:t.noteRegionMap,F.noteRegionMap,!1),palette:(o=vo(t==null?void 0:t.palette))!=null?o:F.palette,performancePreset:(i=xo(t==null?void 0:t.performancePreset))!=null?i:F.performancePreset,enabledLobes:Le(t==null?void 0:t.enabledLobes),pinnedNodePositions:Lo(t==null?void 0:t.pinnedNodePositions),defaultKind:(n=Xe(t==null?void 0:t.defaultKind))!=null?n:F.defaultKind,inferKindsFromLinks:(a=t==null?void 0:t.inferKindsFromLinks)!=null?a:F.inferKindsFromLinks,rendererMode:(c=yo(t==null?void 0:t.rendererMode))!=null?c:F.rendererMode}}function he(t){let r=t.indexOf(":");if(r<0)return null;let e=t.slice(0,r).trim().toLowerCase(),o=t.slice(r+1),i=ut(o);return!e||!i?null:`${e}:${i}`}function Pe(t,r){let e=t.trim().toLowerCase();return e?dt(r).map(o=>`${e}:${o}`):[]}function vo(t){return typeof t!="string"?null:mo.includes(t)?t:null}function xo(t){return typeof t!="string"?null:bo.includes(t)?t:null}function yo(t){return typeof t!="string"?null:go.includes(t)?t:null}function Lo(t){if(!t||typeof t!="object"||Array.isArray(t))return{};let r={};for(let[e,o]of Object.entries(t)){if(!e||!o||typeof o!="object"||Array.isArray(o))continue;let i=o;typeof i.x!="number"||!Number.isFinite(i.x)||typeof i.y!="number"||!Number.isFinite(i.y)||typeof i.z!="number"||!Number.isFinite(i.z)||(r[e]=Ae(i))}return r}function Ae(t){return{x:Ye(t.x,-1.15,1.15),y:Ye(t.y,-1.05,.98),z:Ye(t.z,-1.3,1.3)}}function Ye(t,r,e){return Math.max(r,Math.min(e,t))}function lt(t,r,e){let o={...r};if(!t||typeof t!="object"||Array.isArray(t))return o;for(let[i,n]of Object.entries(t)){let a=ct(i,e),c=Xe(n);!a||!c||(o[a]=c)}return o}function Co(t,r){let e={...r};if(!t||typeof t!="object"||Array.isArray(t))return e;for(let[o,i]of Object.entries(t)){let n=he(o),a=Xe(i);!n||!a||(e[n]=a)}return e}function Po(t,r){let e={...r};if(!t||typeof t!="object"||Array.isArray(t))return e;for(let[o,i]of Object.entries(t)){let n=he(o),a=Y(i);!n||!a||(e[n]=a)}return e}function je(t,r,e){let o={...r};if(!t||typeof t!="object"||Array.isArray(t))return o;for(let[i,n]of Object.entries(t)){let a=ct(i,e),c=Y(n);!a||!c||(o[a]=c)}return o}function ct(t,r){let e=t.replace(/^#/,"").trim();return r?e.toLowerCase():e}function dt(t){if(Array.isArray(t))return t.flatMap(dt);let r=ut(t);return r?[r]:[]}function ut(t){return typeof t!="string"&&typeof t!="number"&&typeof t!="boolean"?null:String(t).replace(/^#/,"").trim().toLowerCase()||null}function Xe(t){var o;if(typeof t!="string")return null;let r=t.trim().replace(/[-_\s]/g,"").toLowerCase(),e=se.find(i=>i.toLowerCase()===r);return(o=e!=null?e:Ao[r])!=null?o:null}function Y(t){var e;if(typeof t!="string")return null;let r=t.trim().replace(/[-_\s]/g,"").toLowerCase();return r==="brainstem"?"stem":(e=k.find(o=>o.toLowerCase()===r))!=null?e:null}var Ao={daily:"dailyNote",dailynote:"dailyNote",journal:"dailyNote",thread:"workThread",workthread:"workThread",moc:"concept",map:"concept",org:"organization",organisation:"organization",company:"organization",repository:"repo",readme:"index"};var E=require("obsidian");var Ro={daily:"dailyNote",dailynote:"dailyNote",journal:"dailyNote",thread:"workThread",workthread:"workThread",moc:"concept",map:"concept",org:"organization",organisation:"organization",company:"organization",repository:"repo",readme:"index"};function le(t){var o;if(typeof t!="string")return null;let r=t.trim().replace(/[-_\s]/g,"").toLowerCase(),e=se.find(i=>i.toLowerCase()===r);return(o=e!=null?e:Ro[r])!=null?o:null}function Re(t,r,e){var a,c;let o=(a=r==null?void 0:r.frontmatter)!=null?a:{},i=ft(o,e.frontmatterKindValueMap);if(i)return{kind:i,source:"frontmatter"};for(let l of e.frontmatterKindKeys){let s=le(o[l]);if(s)return{kind:s,source:"frontmatter"}}for(let l of pt(r)){let s=e.tagKindMap[l];if(s)return{kind:s,source:"tag"}}for(let l of ht(t.path)){let s=(c=e.folderKindMap[l])!=null?c:e.folderKindMap[l.toLowerCase()];if(s)return{kind:s,source:"folder"}}let n=Eo(t.basename,e);return n?{kind:n,source:"filename"}:{kind:e.defaultKind,source:"default"}}function Ee(t,r,e){var a,c;let o=e.noteRegionMap[t.path];if(o)return{lobe:o,source:"note"};let i=(a=r==null?void 0:r.frontmatter)!=null?a:{},n=ft(i,e.frontmatterRegionValueMap);if(n)return{lobe:n,source:"frontmatter"};for(let l of e.frontmatterRegionKeys){let s=Y(i[l]);if(s)return{lobe:s,source:"frontmatter"}}for(let l of pt(r)){let s=e.tagRegionMap[l];if(s)return{lobe:s,source:"tag"}}for(let l of ht(t.path)){let s=(c=e.folderRegionMap[l])!=null?c:e.folderRegionMap[l.toLowerCase()];if(s)return{lobe:s,source:"folder"}}return null}function ft(t,r){for(let[e,o]of Object.entries(t))for(let i of Pe(e,o)){let n=r[i];if(n)return n}return null}function pt(t){var e;return((e=t==null?void 0:t.tags)!=null?e:[]).map(o=>o.replace(/^#/,"").trim().toLowerCase()).filter(Boolean)}function ht(t){return t.split("/").slice(0,-1).flatMap(e=>[e,e.toLowerCase()])}function Eo(t,r){if(r.treatDateFilesAsDaily&&/^\d{4}-\d{2}-\d{2}/.test(t))return"dailyNote";let e=t.trim().toLowerCase();return/(^|[\s-])moc$/.test(e)||e.startsWith("map of ")?"concept":["home","index","_readme","readme"].includes(e)?"index":null}var Q={graphite:{label:"GRAPHITE",bg:"#16151a",bgFar:"#0c0b0e",fg:"#e8e6e0",hud:"#c9b896",chroma:.4,kinds:{person:"#d4d0c4",project:"#c9b896",concept:"#a8b3a0",decision:"#d4b878",question:"#c89878",tool:"#9aa4ac",workThread:"#b89898",dailyNote:"#c9b896",source:"#a8b0bc",repo:"#a89cb0",incident:"#c47878",organization:"#c0b888",index:"#bcc4cc",unknown:"#8e8a82"}},ink:{label:"INK & PAPER",bg:"#0a0a0c",bgFar:"#040405",fg:"#d8d4cc",hud:"#b8a888",chroma:.3,kinds:{person:"#c8c4bc",project:"#b8a888",concept:"#9cb0a4",decision:"#c4a878",question:"#b89878",tool:"#909aa4",workThread:"#a89090",dailyNote:"#c4a878",source:"#98a4b4",repo:"#9890a8",incident:"#b06868",organization:"#b8b080",index:"#b0b8c0",unknown:"#7a7670"}},magma:{label:"MAGMA",bg:"#0a0306",bgFar:"#000000",fg:"#ffe9d8",hud:"#ffc15e",chroma:1,kinds:{person:"#ff6b9d",project:"#ff8a3d",concept:"#ffd93d",decision:"#ff3c6f",question:"#9d3cff",tool:"#ff6b35",workThread:"#ff2e93",dailyNote:"#ffc15e",source:"#c47bff",repo:"#7c2ddb",incident:"#ff1744",organization:"#ffeb3b",index:"#ffdf80",unknown:"#c4a07a"}},bio:{label:"BIOLUMINESCENT",bg:"#001318",bgFar:"#00060a",fg:"#caf0f8",hud:"#00f5d4",chroma:1,kinds:{person:"#00f5d4",project:"#ff006e",concept:"#aaff00",decision:"#ffbe0b",question:"#ff5400",tool:"#8338ec",workThread:"#fb5607",dailyNote:"#06ffa5",source:"#3a86ff",repo:"#7209b7",incident:"#ff006e",organization:"#ffbe0b",index:"#caf0f8",unknown:"#8da9b0"}},acid:{label:"ACID HOUSE",bg:"#06000a",bgFar:"#000000",fg:"#f0ffd0",hud:"#bfff00",chroma:1.15,kinds:{person:"#ff1cb0",project:"#bfff00",concept:"#00fff0",decision:"#ffe800",question:"#ff5c00",tool:"#c800ff",workThread:"#ff007a",dailyNote:"#bfff00",source:"#00b6ff",repo:"#7a00ff",incident:"#ff003c",organization:"#fff200",index:"#ccff80",unknown:"#9a9aa0"}},aurora:{label:"AURORA",bg:"#03040a",bgFar:"#000000",fg:"#e6efff",hud:"#7cf0ff",chroma:.85,kinds:{person:"#7cf0ff",project:"#a07bff",concept:"#7affc1",decision:"#ffd23d",question:"#ff8a3d",tool:"#62a0d0",workThread:"#ff7bdc",dailyNote:"#ffb27a",source:"#9bd2ff",repo:"#b07cff",incident:"#ff5d8f",organization:"#f0ff7a",index:"#cfe9ff",unknown:"#9aa9bd"}},daylight:{label:"DAYLIGHT",bg:"#f7f4ec",bgFar:"#e7dfd2",fg:"#22303a",hud:"#536a7a",chroma:.5,kinds:{person:"#385b6f",project:"#8a5f18",concept:"#52704f",decision:"#9a6a22",question:"#a14f42",tool:"#536979",workThread:"#7c5c76",dailyNote:"#9a6a22",source:"#456c9a",repo:"#6c5f8f",incident:"#a44242",organization:"#6f7435",index:"#4f6670",unknown:"#7a746c"}}},mt={wobbleAmp:.018,wobbleSpeed:.6,halo:.6,bloom:.5,blob:0,jitter:1},qe={person:"PERSON",project:"PROJECT",concept:"CONCEPT",decision:"DECISION",question:"QUESTION",tool:"TOOL",workThread:"THREAD",dailyNote:"DAILY",source:"SOURCE",repo:"REPO",incident:"INCIDENT",organization:"ORG",index:"INDEX",unknown:"UNKNOWN"},Or={...Q.graphite.kinds};var M={frontal:{c:{x:0,y:.2,z:.85},r:.45,label:"FRONTAL"},parietal:{c:{x:0,y:.65,z:-.1},r:.4,label:"PARIETAL"},temporal:{c:{x:.65,y:-.15,z:.1},r:.32,label:"TEMPORAL",mirror:!0},occipital:{c:{x:0,y:.05,z:-.95},r:.36,label:"OCCIPITAL"},cerebellum:{c:{x:0,y:-.55,z:-.78},r:.32,label:"CEREBELLUM"},stem:{c:{x:0,y:-.85,z:-.45},r:.14,label:"BRAIN STEM"}},ee={decision:"frontal",question:"frontal",project:"frontal",concept:"parietal",tool:"parietal",workThread:"parietal",person:"temporal",organization:"temporal",source:"occipital",repo:"occipital",dailyNote:"cerebellum",incident:"cerebellum",index:"stem"};function bt(t,r,e=.03){let o=Math.cos(r),i=Math.sin(r),n=Math.cos(t),a=Math.sin(t),c=.95*o*a,l=1.25*o*n,s=.92*i;l<-.4&&(l-=.06*(-l-.4)),l>.4&&s>-.1&&(c*=1+.05*Math.min(.6,l*(s+.4))),s<-.4&&(s=-.4+(s+.4)*.55),s>.55&&Math.abs(c)<.12&&(s-=.04*(s-.55)*(1-Math.abs(c)/.12));let u=e*(Math.sin(t*11+r*7)+.55*Math.sin(t*17-r*5)+.35*Math.sin(t*5+r*13)),f=Math.sqrt(c*c+s*s+l*l)||1;return c+=c/f*u,s+=s/f*u,l+=l/f*u,{x:c,y:s,z:l}}function So(t,r){let e=Math.cos(r),o=Math.sin(r),i=.02*Math.sin(t*14+r*9);return{x:(.4+i)*e*Math.sin(t),y:-.55+.26*o,z:-.78+(.32+i)*e*Math.cos(t)}}function No(t,r){return{x:r*.06,y:-.55-t*.45,z:-.55+r*.04}}function wo(t,r=.03){let e=[],o=Math.PI*(3-Math.sqrt(5));for(let i=0;i<t;i+=1){let n=(i+.5)/t,a=Math.asin(2*n-1),c=o*i%(Math.PI*2);e.push({...bt(c,a,r),theta:c,phi:a})}return e}function Bo(t){let{x:r,y:e,z:o}=t;return e<-.3&&o<-.45?"cerebellum":e<-.5&&Math.abs(o)<.45&&Math.abs(r)<.25?"stem":o>.3?"frontal":o<-.55?"occipital":e<-.05&&Math.abs(r)>.3?"temporal":e>.2?"parietal":"temporal"}function Do(t){var a;let r=(a=t.dist)!=null?a:3.5,e=Math.cos(t.rotY),o=Math.sin(t.rotY),i=Math.cos(t.rotX),n=Math.sin(t.rotX);return c=>{let l=c.x*e+c.z*o,s=-c.x*o+c.z*e,u=c.y*i-s*n,f=c.y*n+s*i,d=t.scale/(r+f);return{sx:t.cx+l*d*r,sy:t.cy-u*d*r,z:f,scale:d*r/t.scale,depth:(f+1.5)/3}}}function me(t){var r,e;for(let o of t){let i=gt(o.id),n=(i&65535)/65535,a=(i>>>16&65535)/65535,c=(Math.imul(i,31)>>>0&65535)/65535,l=(e=(r=o._lobeName)!=null?r:ee[o.kind])!=null?e:"parietal",s=M[l],u=Mo(o,l,s.r),f=n*Math.PI*2,d=Math.acos(2*a-1),b=s.r*(o.hub?.08:.08+c*.13),m=b*Math.sin(d)*Math.cos(f),g=b*Math.sin(d)*Math.sin(f),x=b*Math.cos(d),v=s.c.x;s.mirror&&n>.5&&(v=-v),o._3dLobe={x:v+u.x+m,y:s.c.y+u.y+g,z:s.c.z+u.z+x},o._lobeName=l}}function Mo(t,r,e){var f;let o=`${r}:${(f=Io(t.path))!=null?f:t.kind}`,i=gt(o),n=(i&65535)/65535,a=(i>>>16&65535)/65535,c=(Math.imul(i,17)>>>0&65535)/65535,l=n*Math.PI*2,s=Math.acos(2*a-1),u=e*(.18+c*.24);return{x:u*Math.sin(s)*Math.cos(l),y:u*Math.sin(s)*Math.sin(l),z:u*Math.cos(s)}}function Io(t){let r=t.indexOf("/");return r<=0?null:t.slice(0,r).toLowerCase()}function gt(t){let r=2166136261;for(let e=0;e<t.length;e+=1)r^=t.charCodeAt(e),r=Math.imul(r,16777619)>>>0;return r}var z={brainPoint:bt,cerebellumPoint:So,stemPoint:No,generateSurface:wo,lobeFor:Bo,makeProjector:Do,assignLobePositions:me,LOBE_CENTERS:M,KIND_TO_LOBE:ee};function Fo(t,r){var m,g,x,v,h;let e=new Map(t.map(p=>[p.file.path,p.file])),o=new Map(t.map(p=>[p.file.basename.toLowerCase(),p.file.path])),i=new Map(t.map(p=>[p.file.path.replace(/\.md$/i,"").toLowerCase(),p.file.path])),n=new Set;for(let p of t){let y=[...(g=(m=p.cache)==null?void 0:m.links)!=null?g:[],...(v=(x=p.cache)==null?void 0:x.embeds)!=null?v:[]];for(let C of y){let L=_o(C.link,p.file.path,o,i,e);!L||L===p.file.path||n.add(zo(p.file.path,L))}}let a=[...n].map(Vo).sort($e),c=vt(a),l=(h=Q[r.palette])!=null?h:Q.graphite,s=t.map(p=>{var B,P,N;let y=Re(p.file,p.cache,r),C=Ee(p.file,p.cache,r),L=(B=c[p.file.path])!=null?B:0,A=Go(y,L,p.file,a,r),R=A.kind;return{id:p.file.path,path:p.file.path,name:p.file.basename,title:p.file.basename,kind:R,kindLabel:(P=qe[R])!=null?P:R.toUpperCase(),status:"active",hub:!1,degree:L,color:(N=l.kinds[R])!=null?N:l.kinds.unknown,classificationSource:A.source,lobeOverrideSource:C==null?void 0:C.source,_lobeName:C==null?void 0:C.lobe}});s=xt(s,r.hubThresholdPercent),s=Ko(s,r.nodeCap);let u=new Set(s.map(p=>p.id));a=a.filter(p=>u.has(p.a)&&u.has(p.b)),a=Ho(a,s,r.edgeCap);let f=vt(a);s=s.map(p=>{var y,C;return{...p,degree:(y=f[p.id])!=null?y:0,color:(C=l.kinds[p.kind])!=null?C:l.kinds.unknown}}),s=xt(s,r.hubThresholdPercent),me(s),Yo(s,r.pinnedNodePositions);let d=Object.fromEntries(s.map(p=>[p.id,p])),b=Uo(s,a);return{nodes:s,edges:a,idx:d,adj:b,KIND_LABEL:qe,activePalette:l,activePaletteName:r.palette,CHAOS:mt}}function yt(t,r){let e=t.vault.getMarkdownFiles().filter(o=>!Ze(t,o.path)).map(o=>({file:To(o),cache:ko(t.metadataCache.getFileCache(o))}));return Fo(e,r)}function Ze(t,r){var o,i;let e=t.metadataCache;return(i=(o=e.isUserIgnored)==null?void 0:o.call(e,r))!=null?i:!1}function To(t){return{path:t.path,basename:t.basename}}function ko(t){var o,i,n,a,c,l,s;let r=(o=t==null?void 0:t.frontmatter)==null?void 0:o.tags,e=[...(n=(i=t==null?void 0:t.tags)==null?void 0:i.map(u=>u.tag))!=null?n:[],...Oo(r)];return{frontmatter:t==null?void 0:t.frontmatter,tags:e,links:(c=(a=t==null?void 0:t.links)==null?void 0:a.map(u=>({link:u.link})))!=null?c:[],embeds:(s=(l=t==null?void 0:t.embeds)==null?void 0:l.map(u=>({link:u.link})))!=null?s:[]}}function Oo(t){return Array.isArray(t)?t.map(String):typeof t=="string"?t.split(/[,\s]+/).filter(Boolean):[]}function _o(t,r,e,o,i){var s,u,f,d;let n=(u=(s=t.split("#")[0])==null?void 0:s.split("^")[0])==null?void 0:u.trim();if(!n)return null;let a=n.endsWith(".md")?n:`${n}.md`;if(i.has(a))return a;let c=r.includes("/")?r.slice(0,r.lastIndexOf("/")):"",l=c?`${c}/${a}`:a;return i.has(l)?l:(d=(f=o.get(n.toLowerCase()))!=null?f:e.get(n.toLowerCase()))!=null?d:null}function zo(t,r){return[t,r].sort((e,o)=>e.localeCompare(o)).join("\0")}function Vo(t){let[r,e]=t.split("\0");return{a:r,b:e}}function $e(t,r){return t.a.localeCompare(r.a)||t.b.localeCompare(r.b)}function vt(t){var e,o;let r={};for(let i of t)r[i.a]=((e=r[i.a])!=null?e:0)+1,r[i.b]=((o=r[i.b])!=null?o:0)+1;return r}function Go(t,r,e,o,i){if(!i.inferKindsFromLinks||t.source!=="default")return t;let n=o.filter(c=>c.b===e.path).length,a=o.filter(c=>c.a===e.path).length;return n>=8&&a<=2?{kind:"index",source:"linkBehavior"}:a>=10&&n<=2?{kind:"source",source:"linkBehavior"}:r>=12&&/index|home|map/i.test(e.basename)?{kind:"index",source:"linkBehavior"}:t}function xt(t,r){if(!t.length)return t;let e=Math.max(0,Math.min(100,r));if(e===0)return t.map(n=>({...n,hub:!1}));let o=Math.max(1,Math.ceil(t.length*(e/100))),i=new Set([...t].filter(n=>n.degree>0).sort((n,a)=>a.degree-n.degree||n.id.localeCompare(a.id)).slice(0,o).map(n=>n.id));return t.map(n=>({...n,hub:i.has(n.id)}))}function Ko(t,r){return t.length<=r?t:[...t].sort((e,o)=>o.degree-e.degree||e.id.localeCompare(o.id)).slice(0,r).sort((e,o)=>e.id.localeCompare(o.id))}function Ho(t,r,e){if(t.length<=e)return t;let o=new Map(r.map(i=>[i.id,i]));return[...t].sort((i,n)=>{var l,s,u,f;let a=((l=o.get(i.a))==null?void 0:l.kind)!==((s=o.get(i.b))==null?void 0:s.kind)?1:0,c=((u=o.get(n.a))==null?void 0:u.kind)!==((f=o.get(n.b))==null?void 0:f.kind)?1:0;return a-c||$e(i,n)}).slice(0,e).sort($e)}function Uo(t,r){var o,i;let e=Object.fromEntries(t.map(n=>[n.id,[]]));for(let n of r)(o=e[n.a])==null||o.push(n.b),(i=e[n.b])==null||i.push(n.a);return e}function Yo(t,r){for(let e of t){let o=r[e.id];o&&(e._3dLobe={...o})}}function Lt(t,r){let e=t.vault.getMarkdownFiles().filter(o=>!Ze(t,o.path)).map(o=>({file:{path:o.path,basename:o.basename},cache:Jo(t.metadataCache.getFileCache(o))}));return jo(e,r)}function jo(t,r){var a,c;let e=qo(),o=$o(),i=Zo(),n=new Map;for(let l of t){let s=Re(l.file,l.cache,r),u=Ee(l.file,l.cache,r),f=(c=(a=u==null?void 0:u.lobe)!=null?a:ee[s.kind])!=null?c:"parietal";e[f]+=1,o[s.source]+=1,u&&(i[u.source]+=1),Wo(n,l,r)}return{totalNotes:t.length,regionCounts:e,sourceCounts:o,lobeOverrideCounts:i,unmappedFrontmatterValues:[...n.values()].sort((l,s)=>s.count-l.count||l.key.localeCompare(s.key)).slice(0,12)}}function Wo(t,r,e){var a,c,l;let o=(c=(a=r.cache)==null?void 0:a.frontmatter)!=null?c:{},i=new Set(e.frontmatterKindKeys.map(s=>s.toLowerCase())),n=new Set(e.frontmatterRegionKeys.map(s=>s.toLowerCase()));for(let[s,u]of Object.entries(o)){let f=s.toLowerCase();for(let d of Pe(s,u)){if(e.frontmatterKindValueMap[d]||e.frontmatterRegionValueMap[d])continue;let b=d.slice(d.indexOf(":")+1);if(i.has(f)&&le(b)||n.has(f)&&Y(b))continue;let m=t.get(d);if(m){m.count+=1;continue}let g=Xo(b),x=(l=ee[g])!=null?l:"parietal";t.set(d,{key:d,field:f,value:b,count:1,examplePath:r.file.path,suggestedKindMapping:`${d}=${g}`,suggestedRegionMapping:`${d}=${x}`})}}}function Xo(t){return/person|people|author|contact|guest|client/.test(t)?"person":/wiki|source|reference|article|book|paper|literature/.test(t)?"source":/project|channel|video|episode|campaign/.test(t)?"project":/meeting|sync|call|thread/.test(t)?"workThread":/daily|journal|log/.test(t)?"dailyNote":/index|moc|map|home/.test(t)?"index":"concept"}function qo(){return Object.fromEntries(k.map(t=>[t,0]))}function $o(){return{frontmatter:0,tag:0,folder:0,filename:0,linkBehavior:0,default:0}}function Zo(){return{note:0,frontmatter:0,tag:0,folder:0}}function Jo(t){var o,i,n,a,c,l,s;let r=(o=t==null?void 0:t.frontmatter)==null?void 0:o.tags,e=[...(n=(i=t==null?void 0:t.tags)==null?void 0:i.map(u=>u.tag))!=null?n:[],...Qo(r)];return{frontmatter:t==null?void 0:t.frontmatter,tags:e,links:(c=(a=t==null?void 0:t.links)==null?void 0:a.map(u=>({link:u.link})))!=null?c:[],embeds:(s=(l=t==null?void 0:t.embeds)==null?void 0:l.map(u=>({link:u.link})))!=null?s:[]}}function Qo(t){return Array.isArray(t)?t.map(String):typeof t=="string"?t.split(/[,\s]+/).filter(Boolean):[]}var Ne=class extends E.PluginSettingTab{constructor(r){super(r.app,r),this.plugin=r}display(){let{containerEl:r}=this;r.empty(),new E.Setting(r).setName("Theme palette").setDesc("Color palette used by the brain renderer.").addDropdown(e=>{for(let o of Object.keys(Q))e.addOption(o,Q[o].label);e.setValue(this.plugin.settings.palette),e.onChange(o=>this.update({palette:o}))}),new E.Setting(r).setName("Performance preset").setDesc("Smooth keeps the current desktop animation rate. Mobile, Balanced, and Battery saver reduce idle frame rate for lower CPU use.").addDropdown(e=>e.addOption("smooth","Smooth (current)").addOption("mobile","Mobile").addOption("balanced","Balanced").addOption("batterySaver","Battery saver").setValue(this.plugin.settings.performancePreset).onChange(o=>this.update({performancePreset:o}))),new E.Setting(r).setName("Renderer").setDesc("Auto uses WebGL2 on desktop and Canvas2D on mobile. Force a renderer for testing or if WebGL has issues.").addDropdown(e=>e.addOption("auto","Auto (recommended)").addOption("webgl2","WebGL2").addOption("canvas2d","Canvas2D").setValue(this.plugin.settings.rendererMode).onChange(o=>this.update({rendererMode:o}))),new E.Setting(r).setName("Node cap").setDesc("Maximum visible notes. Lowest-degree notes are dropped first.").addSlider(e=>e.setLimits(200,1e4,100).setValue(this.plugin.settings.nodeCap).setDynamicTooltip().onChange(o=>this.update({nodeCap:o}))),new E.Setting(r).setName("Edge cap").setDesc("Maximum rendered links.").addSlider(e=>e.setLimits(200,2e4,100).setValue(this.plugin.settings.edgeCap).setDynamicTooltip().onChange(o=>this.update({edgeCap:o}))),new E.Setting(r).setName("Idle auto-rotate").setDesc("Resume slow rotation after interaction pauses.").addToggle(e=>e.setValue(this.plugin.settings.idleAutoRotate).onChange(o=>this.update({idleAutoRotate:o}))),new E.Setting(r).setName("Show labels").setDesc("Draw region callouts and note labels on the brain canvas.").addToggle(e=>e.setValue(this.plugin.settings.showLobeLabels).onChange(o=>this.update({showLobeLabels:o}))),new E.Setting(r).setName("Show legend chip").setDesc("Show the anatomical region legend.").addToggle(e=>e.setValue(this.plugin.settings.showLegendChip).onChange(o=>this.update({showLegendChip:o}))),new E.Setting(r).setName("Pinned positions").setDesc(`${Object.keys(this.plugin.settings.pinnedNodePositions).length} nodes pinned by dragging.`).addButton(e=>e.setButtonText("Reset").onClick(()=>void this.update({pinnedNodePositions:{}}))),new E.Setting(r).setName("Visible regions").setHeading();for(let e of k)new E.Setting(r).setName(Ct(M[e].label)).setDesc("Dim or restore this brain region in the atlas.").addToggle(o=>o.setValue(this.plugin.settings.enabledLobes[e]).onChange(i=>this.update({enabledLobes:Ce(this.plugin.settings.enabledLobes,e,i)})));new E.Setting(r).setName("Click action").setDesc("Choose where clicked notes open.").addDropdown(e=>e.addOption("current","Open in current pane").addOption("new-pane","Open in new pane").addOption("hover-preview","Hover preview").setValue(this.plugin.settings.clickAction).onChange(o=>this.update({clickAction:o}))),new E.Setting(r).setName("Categorization").setHeading(),new E.Setting(r).setName("Default category").setDesc("Category used when no frontmatter, tag, folder, filename, or link rule matches.").addDropdown(e=>{for(let o of se)e.addOption(o,er(o));e.setValue(this.plugin.settings.defaultKind).onChange(o=>this.update({defaultKind:o}))}),new E.Setting(r).setName("Infer categories from links").setDesc("Let uncategorized high-link notes become index or source notes when link structure strongly suggests it.").addToggle(e=>e.setValue(this.plugin.settings.inferKindsFromLinks).onChange(o=>this.update({inferKindsFromLinks:o}))),new E.Setting(r).setName("Frontmatter kind keys").setDesc("Comma-separated frontmatter fields checked for kind/type/category.").addText(e=>e.setValue(this.plugin.settings.frontmatterKindKeys.join(", ")).onChange(o=>this.update({frontmatterKindKeys:o.split(",").map(i=>i.trim()).filter(Boolean)}))),new E.Setting(r).setName("Frontmatter value mappings").setDesc("One per line: field:value=category. Example: type:wiki=source.").addTextArea(e=>{e.setValue(Je(this.plugin.settings.frontmatterKindValueMap)),e.inputEl.rows=6,e.inputEl.placeholder=`type:wiki=source
type:person=person
class:meeting=workThread`,e.inputEl.addEventListener("blur",()=>void this.update({frontmatterKindValueMap:tr(e.getValue())}))}),new E.Setting(r).setName("Tag mappings").setDesc("One per line: tag=category. Tags do not need #.").addTextArea(e=>{e.setValue(Je(this.plugin.settings.tagKindMap)),e.inputEl.rows=8,e.inputEl.addEventListener("blur",()=>void this.update({tagKindMap:Pt(e.getValue(),!0)}))}),new E.Setting(r).setName("Folder mappings").setDesc("One per line: folder=category. Folder names are matched against any path ancestor.").addTextArea(e=>{e.setValue(Je(this.plugin.settings.folderKindMap)),e.inputEl.rows=8,e.inputEl.addEventListener("blur",()=>void this.update({folderKindMap:Pt(e.getValue(),!1)}))}),this.renderClassificationReport(r),new E.Setting(r).setName("Region overrides").setHeading(),new E.Setting(r).setName("Frontmatter region keys").setDesc("Comma-separated frontmatter field names. Example: brain_region, lobe, region. Valid regions: frontal, parietal, temporal, occipital, cerebellum, stem.").addText(e=>{e.inputEl.placeholder="brain_region, lobe, region",e.setValue(this.plugin.settings.frontmatterRegionKeys.join(", ")).onChange(o=>this.update({frontmatterRegionKeys:o.split(",").map(i=>i.trim()).filter(Boolean)}))}),new E.Setting(r).setName("Frontmatter region value mappings").setDesc("One per line: field:value=region. Example: type:wiki=occipital.").addTextArea(e=>{e.setValue(Se(this.plugin.settings.frontmatterRegionValueMap)),e.inputEl.rows=6,e.inputEl.placeholder=`type:wiki=occipital
type:person=temporal`,e.inputEl.addEventListener("blur",()=>void this.update({frontmatterRegionValueMap:or(e.getValue())}))}),new E.Setting(r).setName("Tag region mappings").setDesc("One per line: tag=region. Omit # from tags. Example: client=temporal. Valid regions: frontal, parietal, temporal, occipital, cerebellum, stem.").addTextArea(e=>{e.setValue(Se(this.plugin.settings.tagRegionMap)),e.inputEl.rows=6,e.inputEl.placeholder=`client=temporal
research=occipital
roadmap=frontal`,e.inputEl.addEventListener("blur",()=>void this.update({tagRegionMap:Qe(e.getValue(),!0)}))}),new E.Setting(r).setName("Folder region mappings").setDesc("One per line: folder=region. Folder names are matched against any path ancestor.").addTextArea(e=>{e.setValue(Se(this.plugin.settings.folderRegionMap)),e.inputEl.rows=6,e.inputEl.placeholder=`Channels=frontal
Wiki=occipital
Inbox=stem`,e.inputEl.addEventListener("blur",()=>void this.update({folderRegionMap:Qe(e.getValue(),!1)}))}),new E.Setting(r).setName("Note region mappings").setDesc("One per line: note/path.md=region. Use the exact vault path. Example: Projects/Big Idea.md=frontal. Valid regions: frontal, parietal, temporal, occipital, cerebellum, stem.").addTextArea(e=>{e.setValue(Se(this.plugin.settings.noteRegionMap)),e.inputEl.rows=6,e.inputEl.placeholder=`Projects/Big Idea.md=frontal
People/Ada.md=temporal`,e.inputEl.addEventListener("blur",()=>void this.update({noteRegionMap:Qe(e.getValue(),!1)}))})}async update(r){this.plugin.settings={...this.plugin.settings,...r},await this.plugin.saveSettings(),this.plugin.refreshActiveBrainViews()}renderClassificationReport(r){new E.Setting(r).setName("Classification report").setHeading();let e=Lt(this.plugin.app,this.plugin.settings),o=r.createDiv({cls:"brain-atlas-settings-report"});o.createEl("p",{text:`${e.totalNotes} Markdown notes analyzed from local metadata.`});let i=k.map(c=>`${Ct(M[c].label)}: ${e.regionCounts[c]}`).join(" - ");o.createEl("p",{text:`Regions: ${i}`}),o.createEl("p",{text:`Sources: frontmatter ${e.sourceCounts.frontmatter}, tags ${e.sourceCounts.tag}, folders ${e.sourceCounts.folder}, filenames ${e.sourceCounts.filename}, link behavior ${e.sourceCounts.linkBehavior}, default ${e.sourceCounts.default}.`}),new E.Setting(r).setName("Unmapped frontmatter values").setHeading();let n=r.createDiv({cls:"brain-atlas-settings-report"});if(!e.unmappedFrontmatterValues.length){n.createEl("p",{text:"No unmapped frontmatter values found."});return}let a=n.createEl("ul");for(let c of e.unmappedFrontmatterValues.slice(0,8))a.createEl("li",{text:`${c.key} - ${c.count} notes. Try ${c.suggestedKindMapping} or ${c.suggestedRegionMapping}.`})}};function Ct(t){return t.charAt(0)+t.slice(1).toLowerCase()}function er(t){switch(t){case"dailyNote":return"Daily note";case"workThread":return"Work thread";default:return t.charAt(0).toUpperCase()+t.slice(1)}}function Je(t){return Object.entries(t).sort(([r],[e])=>r.localeCompare(e)).map(([r,e])=>`${r}=${e}`).join(`
`)}function Se(t){return Object.entries(t).sort(([r],[e])=>r.localeCompare(e)).map(([r,e])=>`${r}=${e}`).join(`
`)}function Pt(t,r){let e={};for(let o of t.split(/[\n,]+/)){let[i,n]=o.split("=");if(!i||!n)continue;let a=i.replace(/^#/,"").trim(),c=le(n);!a||!c||(e[r?a.toLowerCase():a]=c)}return e}function tr(t){let r={};for(let e of t.split(/\n+/)){let[o,i]=At(e);if(!o||!i)continue;let n=he(o),a=le(i);!n||!a||(r[n]=a)}return r}function or(t){let r={};for(let e of t.split(/\n+/)){let[o,i]=At(e);if(!o||!i)continue;let n=he(o),a=Y(i);!n||!a||(r[n]=a)}return r}function Qe(t,r){let e={};for(let o of t.split(/[\n,]+/)){let[i,n]=o.split("=");if(!i||!n)continue;let a=i.replace(/^#/,"").trim(),c=Y(n);!a||!c||(e[r?a.toLowerCase():a]=c)}return e}function At(t){let r=t.lastIndexOf("=");return r<0?[null,null]:[t.slice(0,r).trim(),t.slice(r+1).trim()]}var fe=require("obsidian");var Rt=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;function be(t){let r=rr(t.name);if(r&&!Rt.test(r))return r;let e=nr(t.path||t.id);return e&&!Rt.test(e)?e:"Untitled note"}function et(t){return t.path||t.id}function rr(t){return t.trim()}function nr(t){var e,o;return((o=(e=t.split(/[\\/]/).filter(Boolean).pop())==null?void 0:e.trim())!=null?o:"").replace(/\.md$/i,"")}function we(){let t=z.generateSurface(1400,.026).map((i,n)=>({...i,lobe:z.lobeFor(i),twPhase:n*.731%(Math.PI*2),twFreq:.4+n%9/12})),r=[],e=Math.PI*(3-Math.sqrt(5));for(let i=0;i<220;i+=1){let n=(i+.5)/220,a=Math.asin(2*n-1),c=e*i%(Math.PI*2);r.push({...z.cerebellumPoint(c,a),lobe:"cerebellum",twPhase:i*.91%(Math.PI*2),twFreq:.5+i%5/8})}let o=[];for(let i=0;i<28;i+=1){let n=i/28*.6,a=i*1.31%1-.5;o.push({...z.stemPoint(n,a),lobe:"stem",twPhase:i*.55,twFreq:.3})}return[...t,...r,...o]}var ir=.55,ar=6,sr={smooth:0,balanced:1e3/30,batterySaver:1e3/20,mobile:1e3/15},lr={frontal:"project",parietal:"concept",temporal:"person",occipital:"source",cerebellum:"dailyNote",stem:"index"},ce=class{constructor(){this.canvas=null;this.getGraph=null;this.options={idleAutoRotate:!0,showLobeLabels:!0,enabledLobes:pe(),performancePreset:"smooth",mobileMode:!1};this.raf=null;this.frameTimeout=null;this.resizeObserver=null;this.rot={x:-.15,y:.55};this.zoom=1;this.drag=null;this.lastUserAt=0;this.suppressClickUntil=0;this.projCache={};this.signals=[];this.lastSpawn=0;this.hoverId=null;this.focusId=null;this.highlightLobe=null;this.width=1;this.height=1;this.dpr=1;this.forcedDpr=null;this.deterministic=!1;this.enabledPasses=null;this.draw=r=>{var s;this.raf=null;let e=this.canvas,o=(s=this.getGraph)==null?void 0:s.call(this);if(!e||!this.isReady()||!o)return;this.ensureLobePositions(o.nodes),!this.drag&&!this.deterministic&&this.options.idleAutoRotate&&r-this.lastUserAt>1800&&(this.rot.y+=65e-5);let i=Math.min(this.width,this.height)*.32*this.zoom,n=this.width/2,a=this.height/2-this.height*.04,c=z.makeProjector({rotX:this.rot.x,rotY:this.rot.y,scale:i,cx:n,cy:a,dist:3.4}),l=o.nodes.filter(u=>u._3dLobe).map(u=>({node:u,...c(u._3dLobe)}));this.projCache=Object.fromEntries(l.map(u=>[u.node.id,u])),this.drawScene(r),this.scheduleNextFrame(this.nextFrameDelay(r))};this.onPointerDown=r=>{var i,n;if(!this.canvas||r.button!==0)return;r.preventDefault(),r.stopPropagation();let e=this.localPoint(r),o=this.hitTestProjected(e.x,e.y);if(o!=null&&o.node._3dLobe){let a=Ae(o.node._3dLobe);this.drag={mode:"node",startX:r.clientX,startY:r.clientY,nodeId:o.node.id,nodeStart:a,screenScale:Math.max(80,this.currentProjectionScale()*Math.max(.4,o.scale)),moved:!1,pointerId:r.pointerId},this.focusId=o.node.id,this.hoverId=o.node.id,(n=(i=this.options).onChange)==null||n.call(i)}else this.drag={mode:"rotate",startX:r.clientX,startY:r.clientY,rotX:this.rot.x,rotY:this.rot.y,moved:!1,pointerId:r.pointerId};this.lastUserAt=performance.now(),this.canvas.setPointerCapture(r.pointerId),this.requestImmediateFrame()};this.onPointerMove=r=>{var i,n,a,c,l,s;if(!this.canvas)return;if(r.stopPropagation(),this.drag){r.preventDefault();let u=r.clientX-this.drag.startX,f=r.clientY-this.drag.startY;if(this.drag.moved=this.drag.moved||Math.hypot(u,f)>3,this.drag.mode==="node"){let d=this.draggedNodePosition(this.drag,u,f);this.drag.latestPosition=d,this.moveNodeTo(this.drag.nodeId,d),this.focusId=this.drag.nodeId,this.hoverId=this.drag.nodeId,(n=(i=this.options).onChange)==null||n.call(i)}else{let d=u/180,b=f/180;this.rot.y=this.drag.rotY+d,this.rot.x=Math.max(-1.4,Math.min(1.4,this.drag.rotX+b))}this.lastUserAt=performance.now(),this.requestImmediateFrame();return}let e=this.localPoint(r),o=this.hitTest(e.x,e.y);((a=o==null?void 0:o.id)!=null?a:null)!==this.hoverId&&(this.hoverId=(c=o==null?void 0:o.id)!=null?c:null,(s=(l=this.options).onChange)==null||s.call(l),this.requestImmediateFrame())};this.onPointerUp=r=>{var n,a,c,l,s,u,f,d,b;r.stopPropagation();let e=this.drag;if(this.drag=null,!e)return;try{(n=this.canvas)==null||n.releasePointerCapture(e.pointerId)}catch(m){}if(e.mode==="node"&&e.moved&&e.latestPosition){let m=(a=this.getGraph)==null?void 0:a.call(this),g=m==null?void 0:m.idx[e.nodeId];g&&((l=(c=this.options).onPinNode)==null||l.call(c,g,e.latestPosition)),this.suppressClickUntil=performance.now()+600,(u=(s=this.options).onChange)==null||u.call(s),this.requestImmediateFrame();return}if(e.moved){this.suppressClickUntil=performance.now()+600;return}let o=this.localPoint(r),i=this.hitTest(o.x,o.y);this.focusId=(f=i==null?void 0:i.id)!=null?f:null,(b=(d=this.options).onChange)==null||b.call(d),this.requestImmediateFrame()};this.onPointerLeave=()=>{var r,e;this.drag||this.hoverId&&(this.hoverId=null,(e=(r=this.options).onChange)==null||e.call(r),this.requestImmediateFrame())};this.onWheel=r=>{r.preventDefault(),r.stopPropagation(),this.zoom*=1-r.deltaY*.0012,this.zoom=Math.max(ir,Math.min(ar,this.zoom)),this.lastUserAt=performance.now(),this.requestImmediateFrame()};this.onContextMenu=r=>{r.preventDefault(),r.stopPropagation(),this.rot={x:-.15,y:.55},this.zoom=1,this.lastUserAt=performance.now(),this.requestImmediateFrame()}}setDeterministic(r){this.deterministic=r}setEnabledPassesForTest(r){this.enabledPasses=r,this.requestImmediateFrame()}passEnabled(r){return!this.enabledPasses||this.enabledPasses.has(r)}setView(r){r.rot&&(this.rot={...r.rot}),typeof r.zoom=="number"&&(this.zoom=r.zoom),typeof r.dpr=="number"&&(this.forcedDpr=r.dpr,this.resize()),this.requestImmediateFrame()}getInteractionTarget(){return this.canvas}start(r,e,o={}){if(this.stop(),!this.acquireSurface(r))throw new Error("Brain Atlas could not acquire a rendering surface.");this.canvas=r,this.getGraph=e,this.options={...this.options,...o},this.lastUserAt=performance.now(),r.addEventListener("pointerdown",this.onPointerDown),r.addEventListener("pointermove",this.onPointerMove),r.addEventListener("pointerup",this.onPointerUp),r.addEventListener("pointercancel",this.onPointerUp),r.addEventListener("pointerleave",this.onPointerLeave),r.addEventListener("wheel",this.onWheel,{passive:!1}),r.addEventListener("contextmenu",this.onContextMenu),this.resizeObserver=new ResizeObserver(()=>this.resize()),this.resizeObserver.observe(r),this.resize(),this.scheduleNextFrame(0)}stop(){var r;this.raf!=null&&window.cancelAnimationFrame(this.raf),this.raf=null,this.frameTimeout!=null&&window.clearTimeout(this.frameTimeout),this.frameTimeout=null,(r=this.resizeObserver)==null||r.disconnect(),this.resizeObserver=null,this.canvas&&(this.canvas.removeEventListener("pointerdown",this.onPointerDown),this.canvas.removeEventListener("pointermove",this.onPointerMove),this.canvas.removeEventListener("pointerup",this.onPointerUp),this.canvas.removeEventListener("pointercancel",this.onPointerUp),this.canvas.removeEventListener("pointerleave",this.onPointerLeave),this.canvas.removeEventListener("wheel",this.onWheel),this.canvas.removeEventListener("contextmenu",this.onContextMenu)),this.releaseSurface(),this.canvas=null,this.getGraph=null,this.drag=null}releaseSurface(){}setOptions(r){this.options={...this.options,...r},this.canvas&&this.isReady()&&("performancePreset"in r||"mobileMode"in r)&&this.resize(),this.requestImmediateFrame()}setHighlightLobe(r){this.highlightLobe=r,this.requestImmediateFrame()}setFocusForTest(r){this.focusId=r,this.requestImmediateFrame()}setHoverForTest(r){this.hoverId=r,this.requestImmediateFrame()}setSignalsForTest(r){this.signals=r,this.requestImmediateFrame()}moveNodeForTest(r,e){this.moveNodeTo(r,e),this.requestImmediateFrame()}renderOnceForTest(r){this.draw(r),this.raf!=null&&(window.cancelAnimationFrame(this.raf),this.raf=null)}getHoveredNode(){var e,o;let r=(e=this.getGraph)==null?void 0:e.call(this);return this.hoverId&&r&&(o=r.idx[this.hoverId])!=null?o:null}getFocusedNode(){var e,o;let r=(e=this.getGraph)==null?void 0:e.call(this);return this.focusId&&r&&(o=r.idx[this.focusId])!=null?o:null}getLobeStats(){var o,i,n;let r=this.emptyLobeStats(),e=(o=this.getGraph)==null?void 0:o.call(this);if(!e)return r;for(let a of e.nodes){let c=(n=(i=a._lobeName)!=null?i:ee[a.kind])!=null?n:"parietal";r[c]+=1}return r}hitTest(r,e){var o,i;return(i=(o=this.hitTestProjected(r,e))==null?void 0:o.node)!=null?i:null}consumeSuppressedClick(){return!this.suppressClickUntil||performance.now()>this.suppressClickUntil?(this.suppressClickUntil=0,!1):(this.suppressClickUntil=0,!0)}hitTestProjected(r,e){let o=null,i=this.hitTolerance();for(let n in this.projCache){let a=this.projCache[n];if(a.z>.4)continue;let c=Math.hypot(r-a.sx,e-a.sy);c<i&&(i=c,o=a)}return o}nextFrameDelay(r){var o;let e=this.effectivePerformancePreset();return e==="smooth"||this.drag||r-this.lastUserAt<700?0:(o=sr[e])!=null?o:0}effectivePerformancePreset(){return this.options.mobileMode&&this.options.performancePreset==="smooth"?"mobile":this.options.performancePreset}scheduleNextFrame(r){if(!(!this.canvas||this.raf!=null||this.frameTimeout!=null)){if(r<=0){this.raf=window.requestAnimationFrame(this.draw);return}this.frameTimeout=window.setTimeout(()=>{this.frameTimeout=null,this.canvas&&(this.raf=window.requestAnimationFrame(this.draw))},r)}}requestImmediateFrame(){this.canvas&&(this.frameTimeout!=null&&(window.clearTimeout(this.frameTimeout),this.frameTimeout=null),this.raf==null&&(this.raf=window.requestAnimationFrame(this.draw)))}localPoint(r){var o;let e=(o=this.canvas)==null?void 0:o.getBoundingClientRect();return e?{x:r.clientX-e.left,y:r.clientY-e.top}:{x:0,y:0}}draggedNodePosition(r,e,o){let i=this.cameraRight(),n=this.cameraUp(),a=e/r.screenScale,c=o/r.screenScale;return Ae({x:r.nodeStart.x+i.x*a-n.x*c,y:r.nodeStart.y+i.y*a-n.y*c,z:r.nodeStart.z+i.z*a-n.z*c})}moveNodeTo(r,e){var n;let o=(n=this.getGraph)==null?void 0:n.call(this),i=o==null?void 0:o.idx[r];i&&(i._3dLobe={...e},this.onNodeMoved(r))}onNodeMoved(r){}cameraRight(){return{x:Math.cos(this.rot.y),y:0,z:Math.sin(this.rot.y)}}cameraUp(){return{x:Math.sin(this.rot.y)*Math.sin(this.rot.x),y:Math.cos(this.rot.x),z:-Math.cos(this.rot.y)*Math.sin(this.rot.x)}}currentProjectionScale(){return Math.min(this.width,this.height)*.32*this.zoom}hitTolerance(){return Math.max(7,18/Math.sqrt(this.zoom))}resize(){var e;if(!this.canvas||!this.isReady())return;let r=this.canvas.getBoundingClientRect();this.width=Math.max(1,r.width),this.height=Math.max(1,r.height),this.dpr=(e=this.forcedDpr)!=null?e:Math.min(this.maxDevicePixelRatio(),window.devicePixelRatio||1),this.resizeSurface(),this.requestImmediateFrame()}maxDevicePixelRatio(){return this.effectivePerformancePreset()==="mobile"?1:2}ensureLobePositions(r){r.some(e=>!e._3dLobe)&&me(r)}emptyLobeStats(){return{frontal:0,parietal:0,temporal:0,occipital:0,cerebellum:0,stem:0}}lobeColor(r,e){var o,i;return(i=e.activePalette.kinds[(o=lr[r])!=null?o:"concept"])!=null?i:e.activePalette.hud}spawnSignals(r,e,o){if(this.deterministic){for(let i=this.signals.length-1;i>=0;i-=1)r-this.signals[i].born>this.signals[i].dur&&this.signals.splice(i,1);return}if(o.length&&r-this.lastSpawn>900){this.lastSpawn=r;let i=o[Math.floor(Math.random()*o.length)],n=Math.random()<.5,a=e.idx[n?i.a:i.b],c=e.idx[n?i.b:i.a];a&&c&&this.signals.push({id:Math.random(),a,b:c,born:r,dur:2400+Math.random()*1100,colA:a.color,colB:c.color})}for(let i=this.signals.length-1;i>=0;i-=1)r-this.signals[i].born>this.signals[i].dur&&this.signals.splice(i,1)}};var cr={frontal:{sub:"Projects - Decisions - Questions",role:"EXECUTIVE"},parietal:{sub:"Concepts - Tools - Threads",role:"INTEGRATION"},temporal:{sub:"People - Organizations",role:"SOCIAL"},occipital:{sub:"Sources - Repos",role:"PERCEPTION"},cerebellum:{sub:"Daily notes - Incidents",role:"TEMPORAL MEMORY"},stem:{sub:"Index - Routing",role:"ROUTING"}};function j(t,r){let e=t.replace("#","");return`rgba(${parseInt(e.slice(0,2),16)},${parseInt(e.slice(2,4),16)},${parseInt(e.slice(4,6),16)},${r})`}function Et(t,r,e,o){t.strokeStyle=j(e,.8*o),t.lineWidth=1,t.beginPath(),t.arc(r.sx,r.sy,4,0,Math.PI*2),t.stroke(),t.fillStyle=j(e,.4*o),t.beginPath(),t.arc(r.sx,r.sy,4,0,Math.PI*2),t.fill()}function dr(t,r,e,o,i,n){Et(t,r,e,o);let a=r.sx+22,c=r.sy-22;t.strokeStyle=j(e,.8*o),t.lineWidth=1,t.beginPath(),t.moveTo(r.sx+2.8,r.sy-2.8),t.lineTo(a-4,c+6),t.stroke(),t.font="600 11px 'JetBrains Mono', monospace",t.textAlign="left",t.fillStyle=j(e,o),t.fillText(i,a,c),t.font="9px 'JetBrains Mono', monospace",t.fillStyle=j(e,.62*o),t.fillText(n,a,c+12)}function Be(t,r,e,o,i,n){var a;t.textBaseline="middle";for(let c in M){let l=c,s=M[l],u=r(s.c);if(u.z>.6)continue;let f=n(l),d=(1-Math.max(0,u.depth-.2))*i(l);if(!(d<.15)&&(dr(t,u,f,d,s.label,`${cr[l].role} - ${(a=o[l])!=null?a:0} nodes`),s.mirror)){let b=r({x:-s.c.x,y:s.c.y,z:s.c.z});b.z<.6&&Et(t,b,f,d)}}}function ur(t,r,e,o){if(r){let c=Math.max(2,Math.floor(e/120)),l=t>500?3:6;return Math.min(c,l)}let i=Math.max(6,Math.floor(e/80)),n=o>=3?34:o>=2?24:14,a=t>1e3?10:t>500?14:n;return Math.min(i,n,a)}function fr(t,r,e,o,i){let n=ur(t.nodes.length,e,o,i);return new Set(r.filter(a=>a.node.hub&&a.z<=.45).sort((a,c)=>c.node.degree-a.node.degree||a.node.id.localeCompare(c.node.id)).slice(0,n).map(a=>a.node.id))}function De(t,r,e,o,i){var f;let{hoverId:n,focusId:a,zoom:c,width:l,mobile:s}=i;t.font="10px 'JetBrains Mono', monospace",t.textAlign="center",t.textBaseline="top";let u=new Set(fr(e,r,s,l,c));if(n&&u.add(n),a){u.add(a);let d=s?Math.max(3,Math.min(8,Math.round(4*c))):Math.max(8,Math.min(30,Math.round(8*c)));for(let b of((f=e.adj[a])!=null?f:[]).slice(0,d))u.add(b)}for(let d of r){if(!u.has(d.node.id)||d.z>.25&&!d.node.hub)continue;let b=pr(d.node)*Math.max(.6,d.scale),m=Math.max(.2,1-d.depth*.7)*o(d.node._lobeName);if(m<.1)continue;let g=be(d.node),x=t.measureText(g).width;t.fillStyle=`rgba(0,0,0,${.5*m})`,t.fillRect(d.sx-x/2-4,d.sy+b+4,x+8,13),t.fillStyle=d.node.id===a?`rgba(255,255,255,${m})`:j(d.node.color,.95*m),t.fillText(g,d.sx,d.sy+b+5)}}function Me(t,r,e,o,i){let n=o-50,a=i-50,c=22;t.strokeStyle=j(e.activePalette.hud,.25),t.lineWidth=1,t.beginPath(),t.arc(n,a,c,0,Math.PI*2),t.stroke();let l=z.makeProjector({rotX:r.x,rotY:r.y,scale:c*4.5,cx:n,cy:a,dist:4}),s=[{name:"L",v:{x:1,y:0,z:0}},{name:"S",v:{x:0,y:1,z:0}},{name:"A",v:{x:0,y:0,z:1}}];for(let u of s){let f=l(u.v),d=1-(f.z+1.5)/3;t.strokeStyle=j(e.activePalette.hud,.3+d*.55),t.beginPath(),t.moveTo(n,a),t.lineTo(f.sx,f.sy),t.stroke(),t.fillStyle=j(e.activePalette.hud,.5+d*.4),t.font="8px 'JetBrains Mono', monospace",t.textAlign="left",t.textBaseline="middle",t.fillText(u.name,f.sx+3,f.sy)}}function pr(t){return t.hub?6.5:2.6+Math.min(3.4,(t.degree||0)*.42)}var J=class extends ce{constructor(){super();this.ctx=null;this.cloud=we()}acquireSurface(e){return this.ctx=e.getContext("2d"),!!this.ctx}isReady(){return!!this.ctx}resizeSurface(){!this.canvas||!this.ctx||(this.canvas.width=Math.floor(this.width*this.dpr),this.canvas.height=Math.floor(this.height*this.dpr),this.ctx.setTransform(this.dpr,0,0,this.dpr,0,0))}releaseSurface(){this.ctx=null}drawScene(e){var v;let o=this.canvas,i=this.ctx,n=(v=this.getGraph)==null?void 0:v.call(this);if(!o||!i||!n)return;let a=n.activePalette,c=Math.min(this.width,this.height)*.32*this.zoom,l=this.width/2,s=this.height/2-this.height*.04,u=z.makeProjector({rotX:this.rot.x,rotY:this.rot.y,scale:c,cx:l,cy:s,dist:3.4}),f=this.getLobeStats(),d=n.edges.filter(h=>{let p=n.idx[h.a],y=n.idx[h.b];return p&&y&&p._lobeName!==y._lobeName}),b=h=>Z(h,this.options.enabledLobes,this.highlightLobe);if(this.spawnSignals(e,n,d),this.passEnabled("background")){let h=i.createRadialGradient(l,s,0,l,s,Math.max(this.width,this.height)*.75);h.addColorStop(0,a.bg),h.addColorStop(.55,a.bg),h.addColorStop(1,a.bgFar),i.fillStyle=h,i.fillRect(0,0,this.width,this.height)}this.passEnabled("haze")&&this.drawLobeHaze(i,u,c,n,b);let m=this.cloud.map(h=>{var p,y;return{p:h,pr:u(h),tw:.65+.35*Math.sin(e*5e-4*((p=h.twFreq)!=null?p:1)+((y=h.twPhase)!=null?y:0))}}),g=n.nodes.filter(h=>h._3dLobe).map(h=>({node:h,...u(h._3dLobe)})),x=this.projectEdges(n,u);if(this.passEnabled("cloud")){i.globalCompositeOperation="lighter";for(let h of m)h.pr.z<=0||this.drawCloudPoint(i,h,!0,n,b);i.globalCompositeOperation="source-over"}if(this.passEnabled("edges"))for(let h of x.filter(p=>p.z>0).sort((p,y)=>y.z-p.z))this.drawEdge(i,h,!0,n,b);if(this.passEnabled("nodes"))for(let h of g.filter(p=>p.z>0).sort((p,y)=>y.z-p.z))this.drawNode(i,h,n,b);if(this.passEnabled("cloud")){i.globalCompositeOperation="lighter";for(let h of m)h.pr.z>0||this.drawCloudPoint(i,h,!1,n,b);i.globalCompositeOperation="source-over"}if(this.passEnabled("edges"))for(let h of x.filter(p=>p.z<=0).sort((p,y)=>y.z-p.z))this.drawEdge(i,h,!1,n,b);if(this.passEnabled("nodes"))for(let h of g.filter(p=>p.z<=0).sort((p,y)=>y.z-p.z))this.drawNode(i,h,n,b);this.passEnabled("signals")&&this.drawSignals(i,e,u,b),this.passEnabled("labels")&&(this.options.showLobeLabels&&this.drawLobeLabels(i,u,n,f,b),this.options.showLobeLabels&&this.drawNodeLabels(i,g,n,b)),this.passEnabled("compass")&&this.drawCompass(i,n)}drawLobeHaze(e,o,i,n,a){let c=[];for(let l in M){let s=l,u=M[s];if(c.push({lobe:s,lobeCenter:u,center:u.c,pr:o(u.c)}),u.mirror){let f={x:-u.c.x,y:u.c.y,z:u.c.z};c.push({lobe:s,lobeCenter:u,center:f,pr:o(f)})}}e.globalCompositeOperation="lighter";for(let l of c.sort((s,u)=>u.pr.z-s.pr.z)){let s=this.lobeColor(l.lobe,n),u=l.lobeCenter.r*i*1.4*l.pr.scale,f=Math.max(.25,1-l.pr.depth*.55),d=(this.highlightLobe===l.lobe?.18:.07)*f*a(l.lobe);if(d<.005)continue;let b=e.createRadialGradient(l.pr.sx,l.pr.sy,0,l.pr.sx,l.pr.sy,u);b.addColorStop(0,V(s,d)),b.addColorStop(.55,V(s,d*.45)),b.addColorStop(1,V(s,0)),e.fillStyle=b,e.beginPath(),e.arc(l.pr.sx,l.pr.sy,u,0,Math.PI*2),e.fill()}e.globalCompositeOperation="source-over"}drawCloudPoint(e,o,i,n,a){var u;let c=(u=o.p.lobe)!=null?u:"parietal",l=i?.2:.38,s=(1-o.pr.depth)*l*o.tw*a(c);e.fillStyle=V(this.lobeColor(c,n),s),e.beginPath(),e.arc(o.pr.sx,o.pr.sy,i?.95:1.2,0,Math.PI*2),e.fill()}projectEdges(e,o){let n=[];for(let a of e.edges){let c=e.idx[a.a],l=e.idx[a.b];if(!(c!=null&&c._3dLobe)||!(l!=null&&l._3dLobe))continue;let s={x:(c._3dLobe.x+l._3dLobe.x)*.35,y:(c._3dLobe.y+l._3dLobe.y)*.35,z:(c._3dLobe.z+l._3dLobe.z)*.35},u=[],f=0;for(let d=0;d<=12;d+=1){let b=d/12,m=1-b,g={x:m*m*c._3dLobe.x+2*m*b*s.x+b*b*l._3dLobe.x,y:m*m*c._3dLobe.y+2*m*b*s.y+b*b*l._3dLobe.y,z:m*m*c._3dLobe.z+2*m*b*s.z+b*b*l._3dLobe.z},x=o(g);u.push(x),f+=x.z}n.push({e:a,A:c,B:l,pts:u,z:f/u.length,sameLobe:c._lobeName===l._lobeName})}return n}drawEdge(e,o,i,n,a){var m,g;let c=this.focusId&&(o.e.a===this.focusId||o.e.b===this.focusId),l=this.hoverId&&(o.e.a===this.hoverId||o.e.b===this.hoverId),s=this.lobeColor((m=o.A._lobeName)!=null?m:"parietal",n),u=this.lobeColor((g=o.B._lobeName)!=null?g:"parietal",n),f=Math.max(a(o.A._lobeName),a(o.B._lobeName)),d=o.sameLobe?1:1.6,b=(c?i?.55:.85:l?i?.25:.4:i?.05:.13)*f*d;e.lineWidth=c?1.3:i?.55:.7;for(let x=0;x<o.pts.length-1;x+=1){let v=o.pts[x],h=o.pts[x+1],p=x/(o.pts.length-1),y=b*(1-(v.depth+h.depth)/2*.35),C=o.sameLobe||p<.5?s:u;e.strokeStyle=V(c?o.A.color:C,y),e.beginPath(),e.moveTo(v.sx,v.sy),e.lineTo(h.sx,h.sy),e.stroke()}}drawNode(e,o,i,n){let a=o.node,c=a.id===this.hoverId,l=a.id===this.focusId,s=hr(a)*Math.max(.55,o.scale)*(c?1.18:l?1.25:1),u=Math.max(.32,1-o.depth*.75),f=a.status==="archived"?.3:a.status==="dormantRelevant"?.55:1,d=u*f*n(a._lobeName);if(d<.05)return;let b=s*3.6*i.CHAOS.halo,m=e.createRadialGradient(o.sx,o.sy,0,o.sx,o.sy,b);m.addColorStop(0,V(a.color,.32*d*i.CHAOS.bloom)),m.addColorStop(1,V(a.color,0)),e.fillStyle=m,e.beginPath(),e.arc(o.sx,o.sy,b,0,Math.PI*2),e.fill(),e.fillStyle=V(a.color,Math.min(1,d*.93)),e.beginPath(),e.arc(o.sx,o.sy,s,0,Math.PI*2),e.fill(),e.fillStyle=`rgba(255,255,255,${Math.min(1,d)})`,e.beginPath(),e.arc(o.sx,o.sy,Math.max(.7,s*.42),0,Math.PI*2),e.fill(),a.hub&&(e.strokeStyle=V(a.color,Math.min(1,.55*d)),e.lineWidth=.8,e.beginPath(),e.arc(o.sx,o.sy,s+4,0,Math.PI*2),e.stroke(),e.strokeStyle=V(a.color,Math.min(1,.45*d)),e.beginPath(),e.moveTo(o.sx-s*3.2,o.sy),e.lineTo(o.sx+s*3.2,o.sy),e.moveTo(o.sx,o.sy-s*3.2),e.lineTo(o.sx,o.sy+s*3.2),e.stroke())}drawSignals(e,o,i,n){e.globalCompositeOperation="lighter";for(let a of this.signals){if(!a.a._3dLobe||!a.b._3dLobe)continue;let c=(o-a.born)/a.dur;if(c<0||c>1)continue;let l=Math.sin(c*Math.PI),s=Math.max(n(a.a._lobeName),n(a.b._lobeName)),u={x:(a.a._3dLobe.x+a.b._3dLobe.x)*.35,y:(a.a._3dLobe.y+a.b._3dLobe.y)*.35,z:(a.a._3dLobe.z+a.b._3dLobe.z)*.35};for(let f=0;f<6;f+=1){let d=Math.max(0,c-f*.035),b=1-d,m={x:b*b*a.a._3dLobe.x+2*b*d*u.x+d*d*a.b._3dLobe.x,y:b*b*a.a._3dLobe.y+2*b*d*u.y+d*d*a.b._3dLobe.y,z:b*b*a.a._3dLobe.z+2*b*d*u.z+d*d*a.b._3dLobe.z},g=i(m),x=mr(a.colA,a.colB,d),v=(1-f/6)*l,h=Math.max(.3,1-g.depth*.6),p=(1.3-f*.15)*Math.max(.5,g.scale),y=e.createRadialGradient(g.sx,g.sy,0,g.sx,g.sy,p*3.2);y.addColorStop(0,tt(x,.22*v*h*s)),y.addColorStop(1,tt(x,0)),e.fillStyle=y,e.beginPath(),e.arc(g.sx,g.sy,p*3.2,0,Math.PI*2),e.fill(),e.fillStyle=tt(x,.55*v*h*s),e.beginPath(),e.arc(g.sx,g.sy,Math.max(.6,p),0,Math.PI*2),e.fill()}}e.globalCompositeOperation="source-over"}drawLobeLabels(e,o,i,n,a){Be(e,o,i,n,a,c=>this.lobeColor(c,i))}drawNodeLabels(e,o,i,n){De(e,o,i,n,{hoverId:this.hoverId,focusId:this.focusId,zoom:this.zoom,width:this.width,mobile:this.effectivePerformancePreset()==="mobile"})}drawCompass(e,o){Me(e,this.rot,o,this.width,this.height)}};function hr(t){return t.hub?6.5:2.6+Math.min(3.4,(t.degree||0)*.42)}function V(t,r){let e=t.replace("#","");return`rgba(${parseInt(e.slice(0,2),16)},${parseInt(e.slice(2,4),16)},${parseInt(e.slice(4,6),16)},${r})`}function mr(t,r,e){let o=t.replace("#",""),i=r.replace("#",""),n=parseInt(o.slice(0,2),16),a=parseInt(o.slice(2,4),16),c=parseInt(o.slice(4,6),16),l=parseInt(i.slice(0,2),16),s=parseInt(i.slice(2,4),16),u=parseInt(i.slice(4,6),16);return`rgb(${Math.round(n+(l-n)*e)},${Math.round(a+(s-a)*e)},${Math.round(c+(u-c)*e)})`}function tt(t,r){return t.replace("rgb(","rgba(").replace(")",`,${r})`)}function St(t,r,e,o){return{rotX:o.x,rotY:o.y,scale:Math.min(t,r)*.32*e,cx:t/2,cy:r/2-r*.04,dist:3.4}}function Ie(t,r){let{rotX:e,rotY:o,scale:i,cx:n,cy:a,dist:c}=t,l=Math.cos(o),s=Math.sin(o),u=Math.cos(e),f=Math.sin(e),d=r.x*l+r.z*s,b=-r.x*s+r.z*l,m=r.y*u-b*f,g=r.y*f+b*u,x=i/(c+g);return{sx:n+d*x*c,sy:a-m*x*c,z:g,scale:x*c/i,depth:(g+1.5)/3}}function W(t){let r=t.startsWith("#")?t.slice(1):t;return[parseInt(r.slice(0,2),16)/255,parseInt(r.slice(2,4),16)/255,parseInt(r.slice(4,6),16)/255]}function Nt(t,r,e){let o=t.createShader(r);if(!o)throw new Error("Failed to create WebGL shader.");if(t.shaderSource(o,e),t.compileShader(o),!t.getShaderParameter(o,t.COMPILE_STATUS)){let i=t.getShaderInfoLog(o);t.deleteShader(o);let n=r===t.VERTEX_SHADER?"vertex":"fragment";throw new Error(`WebGL ${n} shader compile failed:
${i!=null?i:"(no log)"}`)}return o}function te(t,r,e){let o=Nt(t,t.VERTEX_SHADER,r),i=Nt(t,t.FRAGMENT_SHADER,e),n=t.createProgram();if(!n)throw t.deleteShader(o),t.deleteShader(i),new Error("Failed to create WebGL program.");if(t.attachShader(n,o),t.attachShader(n,i),t.linkProgram(n),t.deleteShader(o),t.deleteShader(i),!t.getProgramParameter(n,t.LINK_STATUS)){let a=t.getProgramInfoLog(n);throw t.deleteProgram(n),new Error(`WebGL program link failed:
${a!=null?a:"(no log)"}`)}return n}function oe(t,r,e){let o={};for(let i of e)o[i]=t.getUniformLocation(r,i);return o}function de(t,r){let e=t.createBuffer();if(!e)throw new Error("Failed to create WebGL buffer.");return t.bindBuffer(t.ARRAY_BUFFER,e),t.bufferData(t.ARRAY_BUFFER,r,t.STATIC_DRAW),e}var wt=`#version 300 es
precision highp float;
in vec2 aPosition;
void main() {
  gl_Position = vec4(aPosition, 0.0, 1.0);
}
`,Bt=`#version 300 es
precision highp float;

uniform vec2 uResolution; // device-pixel framebuffer size (w, h)
uniform float uDpr;       // device pixel ratio
uniform vec2 uCenter;     // gradient center in CSS px (cx, cy)
uniform float uRadius;    // gradient radius in CSS px (max(w,h) * 0.75)
uniform vec3 uBg;         // inner color, stored sRGB [0,1]
uniform vec3 uBgFar;      // outer color, stored sRGB [0,1]

out vec4 outColor;

void main() {
  // gl_FragCoord: device px, origin bottom-left. Convert to CSS px, top-left.
  vec2 cssPx = vec2(gl_FragCoord.x, uResolution.y - gl_FragCoord.y) / uDpr;

  // resize() guarantees width/height >= 1, so uRadius = max(w,h)*0.75 >= 0.75; division by zero cannot occur.
  float t = clamp(distance(cssPx, uCenter) / uRadius, 0.0, 1.0);

  // Stops: bg @0, bg @0.55, bgFar @1 (interpolate in stored sRGB space).
  vec3 c = t <= 0.55 ? uBg : mix(uBg, uBgFar, (t - 0.55) / 0.45);

  // Premultiplied, opaque: alpha 1.0 => premultiplied == straight.
  outColor = vec4(c, 1.0);
}
`,Dt=`#version 300 es
precision highp float;

in vec2 aPosition;        // unit quad [-1, 1]\xB2, same buffer as background

uniform vec2 uResolution; // device-pixel framebuffer size (w, h)
uniform float uDpr;       // device pixel ratio
uniform vec2 uCenter;     // quad center in CSS px
uniform float uRadius;    // half-side in CSS px

void main() {
  // Map the unit quad vertex to a CSS-px position:
  //   center + aPosition * radius
  vec2 cssPx = uCenter + aPosition * uRadius;

  // Convert CSS px \u2192 NDC clip space.
  // CSS px origin is top-left; clip space origin is center with Y pointing up.
  // Step 1: convert to device px (multiply by dpr).
  // Step 2: normalize to [0,1] range in device pixels.
  // Step 3: remap to [-1,1] and flip Y (CSS top-left \u2192 GL bottom-left).
  vec2 devPx = cssPx * uDpr;
  vec2 ndc = (devPx / uResolution) * 2.0 - 1.0;
  ndc.y = -ndc.y;

  gl_Position = vec4(ndc, 0.0, 1.0);
}
`,Mt=`#version 300 es
precision highp float;

uniform vec2 uResolution; // device-pixel framebuffer size (w, h)
uniform float uDpr;       // device pixel ratio
uniform vec2 uCenter;     // gradient center in CSS px
uniform float uRadius;    // gradient radius in CSS px
uniform vec3 uColor;      // lobe color, stored sRGB [0,1]
uniform float uBaseA;     // base alpha at t=0

out vec4 outColor;

void main() {
  // Convert fragment position to CSS px, top-left origin (same as Canvas2D).
  vec2 cssPx = vec2(gl_FragCoord.x, uResolution.y - gl_FragCoord.y) / uDpr;

  // Radial distance parameter, clamped to [0, 1].
  float t = clamp(distance(cssPx, uCenter) / uRadius, 0.0, 1.0);

  // Piecewise linear alpha matching Canvas2D radialGradient stops:
  //   stop 0.00 -> baseA
  //   stop 0.55 -> baseA * 0.45
  //   stop 1.00 -> 0
  float alpha;
  if (t <= 0.55) {
    alpha = mix(uBaseA, uBaseA * 0.45, t / 0.55);
  } else {
    alpha = mix(uBaseA * 0.45, 0.0, (t - 0.55) / 0.45);
  }

  // Premultiplied additive output: with blendFunc(ONE, ONE) this correctly
  // accumulates multiple halos regardless of draw order (additive is commutative).
  outColor = vec4(uColor * alpha, alpha);
}
`,It=`#version 300 es
precision highp float;

in vec3 aPosition;    // model-space xyz
in float aLobeIndex;  // lobe index 0-5 (stored as float; integer-valued)
in float aPhase;      // twinkle phase
in float aFreq;       // twinkle frequency
in vec2 aCorner;      // quad corner offset in [-1, 1]^2

uniform vec2 uResolution;   // device-pixel framebuffer size (w, h)
uniform float uDpr;         // device pixel ratio
// Projection inputs (same values as ProjectionOpts / makeProjector).
uniform float uRotX;
uniform float uRotY;
uniform float uSceneScale;  // min(w,h) * 0.32 * zoom
uniform float uCx;
uniform float uCy;
uniform float uDist;        // 3.4
uniform float uTime;        // injected timestamp (ms) \u2014 twinkle clock
uniform float uHemisphere;  // +1.0 = far pass (z>0), -1.0 = near pass (z<=0)
uniform float uLobeMul[6];  // lobeVisibilityMultiplier per lobe

out vec2 vCornerDev;        // corner offset from sprite center, in device px
out float vRadiusDev;       // sprite radius in device px
out float vAlpha;           // per-point straight alpha
flat out int vLobe;         // lobe index (for color lookup in FS)

void main() {
  // ---- Projection (inlined from projection.ts projectPoint) ----
  float cosY = cos(uRotY);
  float sinY = sin(uRotY);
  float cosX = cos(uRotX);
  float sinX = sin(uRotX);

  float rotatedX = aPosition.x * cosY + aPosition.z * sinY;
  float z1 = -aPosition.x * sinY + aPosition.z * cosY;
  float rotatedY = aPosition.y * cosX - z1 * sinX;
  float z2 = aPosition.y * sinX + z1 * cosX;

  float f = uSceneScale / (uDist + z2);
  float sx = uCx + rotatedX * f * uDist;          // CSS px
  float sy = uCy - rotatedY * f * uDist;          // CSS px
  float depth = (z2 + 1.5) / 3.0;

  // far = projected z > 0 (matches drawCloudPoint's far classification).
  bool far = z2 > 0.0;

  // Hemisphere cull: drop the quad if its far-ness != the requested pass.
  bool wantFar = uHemisphere > 0.0;
  if (far != wantFar) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0); // outside clip space \u2192 culled
    vCornerDev = vec2(0.0);
    vRadiusDev = 0.0;
    vAlpha = 0.0;
    vLobe = 0;
    return;
  }

  // Per-point alpha (drawCloudPoint).
  float alphaBase = far ? 0.20 : 0.38;
  float tw = 0.65 + 0.35 * sin(uTime * 0.0005 * aFreq + aPhase);
  int lobe = int(aLobeIndex + 0.5);
  float lobeMul = uLobeMul[lobe];
  vAlpha = (1.0 - depth) * alphaBase * tw * lobeMul;
  vLobe = lobe;

  // Screen radius in CSS px, then device px for the analytic-coverage circle.
  float radiusCss = far ? 0.95 : 1.2;
  float radiusDev = radiusCss * uDpr;
  vRadiusDev = radiusDev;
  vCornerDev = aCorner * radiusDev;

  // Place the quad corner at screen(sx,sy) + corner * radius (CSS px), then
  // convert to clip space using the same dpr / Y-flip convention as bg/haze.
  vec2 cssPx = vec2(sx, sy) + aCorner * radiusCss;
  vec2 devPx = cssPx * uDpr;
  vec2 ndc = (devPx / uResolution) * 2.0 - 1.0;
  ndc.y = -ndc.y;
  gl_Position = vec4(ndc, 0.0, 1.0);
}
`,Ft=`#version 300 es
precision highp float;

uniform vec3 uLobeColors[6]; // lobe colors, stored sRGB [0,1]

in vec2 vCornerDev;   // corner offset from sprite center (device px)
in float vRadiusDev;  // sprite radius (device px)
in float vAlpha;      // per-point straight alpha
flat in int vLobe;    // lobe index

out vec4 outColor;

void main() {
  // Distance from sprite center in device px.
  float dist = length(vCornerDev);
  // ~1 device-px analytic AA edge approximating Canvas2D arc()+fill.
  float coverage = clamp(vRadiusDev - dist + 0.5, 0.0, 1.0);

  float a = vAlpha * coverage;
  vec3 color = uLobeColors[vLobe];

  // Premultiplied additive output (blendFunc(ONE, ONE)).
  outColor = vec4(color * a, a);
}
`,Tt=`#version 300 es
precision highp float;

in vec3 aPosition;     // model xyz, this centerline point (segment END at the provoking vertex)
in vec3 aTangentRef;   // model xyz of the next centerline point (for screen tangent)
in vec3 aSegStartRef;  // model xyz of the provoked segment's START point (p0)
in float aSide;        // extrusion side -1 / +1
in vec3 aColorA;       // lobe A rgb
in vec3 aColorB;       // lobe B rgb
in vec3 aFocusColor;   // edge.A.color rgb (focus override)
in float aSameLobe;    // 1 = same lobe, 0 = inter-lobe
in float aColorSelector; // flat: 0 = cA, 1 = cB (provoking-vertex corrected)
in float aLobeIdxA;    // lobe index 0-5 of endpoint A
in float aLobeIdxB;    // lobe index 0-5 of endpoint B
in float aNodeIdxA;    // node-buffer index of endpoint A
in float aNodeIdxB;    // node-buffer index of endpoint B

uniform vec2 uResolution;  // device-px framebuffer size (w, h)
uniform float uDpr;        // device pixel ratio
uniform float uRotX;
uniform float uRotY;
uniform float uSceneScale; // min(w,h) * 0.32 * zoom
uniform float uCx;
uniform float uCy;
uniform float uDist;       // 3.4
uniform float uIsFar;      // +1.0 = far pass (mean z > 0), 0.0 = near pass
uniform float uLobeMul[6]; // lobeVisibilityMultiplier per lobe
uniform float uFocusNodeIndex; // node index of focus node, or -1
uniform float uHoverNodeIndex; // node index of hover node, or -1

flat out vec3 vColor;        // per-segment color (cA / cB / focus override)
flat out float vAlpha;       // per-segment constant alpha (stair-step)
flat out float vHalfWidthDev; // half line width in device px (for AA coverage)
out float vDistFromCenter;   // signed distance from centerline in device px

// Project a model point to CSS-px screen position; also returns depth via out param.
vec2 projectCss(vec3 p, float cosX, float sinX, float cosY, float sinY, out float depth) {
  float rotatedX = p.x * cosY + p.z * sinY;
  float z1 = -p.x * sinY + p.z * cosY;
  float rotatedY = p.y * cosX - z1 * sinX;
  float z2 = p.y * sinX + z1 * cosX;
  float f = uSceneScale / (uDist + z2);
  depth = (z2 + 1.5) / 3.0;
  return vec2(uCx + rotatedX * f * uDist, uCy - rotatedY * f * uDist);
}

void main() {
  float cosY = cos(uRotY);
  float sinY = sin(uRotY);
  float cosX = cos(uRotX);
  float sinX = sin(uRotX);

  // Project this centerline point + the tangent reference + the segment-start point.
  float depthThis, depthTan, depthStart;
  vec2 cssThis = projectCss(aPosition, cosX, sinX, cosY, sinY, depthThis);
  vec2 cssTan  = projectCss(aTangentRef, cosX, sinX, cosY, sinY, depthTan);
  vec2 cssStart = projectCss(aSegStartRef, cosX, sinX, cosY, sinY, depthStart);

  // ---- Per-edge dynamic values (drawEdge) computed in-shader ----
  int lobeA = int(aLobeIdxA + 0.5);
  int lobeB = int(aLobeIdxB + 0.5);
  float lobeM = max(uLobeMul[lobeA], uLobeMul[lobeB]);
  float interBoost = aSameLobe > 0.5 ? 1.0 : 1.6;

  bool isFar = uIsFar > 0.5;

  float fIdx = uFocusNodeIndex;
  float hIdx = uHoverNodeIndex;
  bool isFocus = fIdx >= 0.0 && (abs(aNodeIdxA - fIdx) < 0.5 || abs(aNodeIdxB - fIdx) < 0.5);
  bool isHover = hIdx >= 0.0 && (abs(aNodeIdxA - hIdx) < 0.5 || abs(aNodeIdxB - hIdx) < 0.5);

  float baseA;
  if (isFocus) {
    baseA = isFar ? 0.55 : 0.85;
  } else if (isHover) {
    baseA = isFar ? 0.25 : 0.40;
  } else {
    baseA = isFar ? 0.05 : 0.13;
  }
  baseA *= lobeM * interBoost;

  float lineWidthCss = isFocus ? 1.3 : (isFar ? 0.55 : 0.7);

  // FLAT per-segment alpha (stair-step): avg of the segment's two endpoint depths.
  // At the provoking vertex (tIdx k+1) aPosition = p1 (segment END), aSegStartRef = p0.
  float avgDepth = (depthStart + depthThis) * 0.5;
  vAlpha = baseA * (1.0 - avgDepth * 0.35);

  // Per-segment color: intra-lobe \u2192 cA; inter-lobe \u2192 cA for segs 0-5, cB for 6-11
  // (delivered via flat aColorSelector). Focus edges override to focusColor.
  vec3 segColor = aColorSelector > 0.5 ? aColorB : aColorA;
  vColor = isFocus ? aFocusColor : segColor;

  // ---- Ribbon extrusion (perpendicular to screen tangent) ----
  // Half line width in device px; +1px AA margin so the FS coverage edge fits.
  float halfWidthDev = lineWidthCss * 0.5 * uDpr;
  vHalfWidthDev = halfWidthDev;
  float extrude = halfWidthDev + 1.0; // device px

  // Screen tangent (CSS px is fine for direction; scale cancels in normalize).
  vec2 dir = cssTan - cssThis;
  float len = length(dir);
  vec2 tdir = len > 1e-6 ? dir / len : vec2(1.0, 0.0);
  vec2 nrm = vec2(-tdir.y, tdir.x); // 90\xB0 rotation \u2192 perpendicular

  vDistFromCenter = aSide * extrude;

  // Centerline in device px, then offset along the perpendicular by side*extrude.
  vec2 devThis = cssThis * uDpr;
  vec2 devPos = devThis + nrm * (aSide * extrude);

  // Device px \u2192 NDC (top-left CSS origin \u2192 GL bottom-left).
  vec2 ndc = (devPos / uResolution) * 2.0 - 1.0;
  ndc.y = -ndc.y;
  gl_Position = vec4(ndc, 0.0, 1.0);
}
`,kt=`#version 300 es
precision highp float;

flat in vec3 vColor;
flat in float vAlpha;
flat in float vHalfWidthDev;
in float vDistFromCenter;

out vec4 outColor;

void main() {
  // Analytic coverage reproducing Canvas2D's sub-pixel lineWidth partial coverage.
  float coverage = clamp(vHalfWidthDev - abs(vDistFromCenter) + 0.5, 0.0, 1.0);
  float a = vAlpha * coverage;

  // Premultiplied source-over output (blendFunc(ONE, ONE_MINUS_SRC_ALPHA)).
  outColor = vec4(vColor * a, a);
}
`,Ot=`#version 300 es
precision highp float;

// Per-vertex attributes (packed from CPU per-frame into a dynamic buffer).
in vec2 aCenter;        // sprite center in CSS px (sx, sy)
in vec2 aCorner;        // quad corner offset [-1,1]^2
in vec3 aColor;         // RGB [0,1]
in float aHaloAlpha;    // halo alpha factor (0.22 * fade * depth * regionAlpha)
in float aCoreAlpha;    // core alpha factor (0.55 * fade * depth * regionAlpha)
in float aHaloRadiusDev;// halo radius in device px (radius * 3.2 * dpr)
in float aCoreRadiusDev;// core radius in device px (max(0.6, radius) * dpr)

uniform vec2 uResolution; // device-px framebuffer size (w, h)
uniform float uDpr;       // device pixel ratio

out vec2 vCornerDev;    // corner offset from sprite center in device px
out vec3 vColor;
out float vHaloAlpha;
out float vCoreAlpha;
out float vHaloRadiusDev;
out float vCoreRadiusDev;

void main() {
  // Bounding half-extent: the larger of halo or core.
  float halfExtentDev = max(aHaloRadiusDev, aCoreRadiusDev);

  // Corner offset in device px.
  vCornerDev = aCorner * halfExtentDev;
  vColor = aColor;
  vHaloAlpha = aHaloAlpha;
  vCoreAlpha = aCoreAlpha;
  vHaloRadiusDev = aHaloRadiusDev;
  vCoreRadiusDev = aCoreRadiusDev;

  // Convert CSS px center + corner to clip space.
  // Corner offset added in CSS px (before dpr multiply).
  float halfExtentCss = halfExtentDev / uDpr;
  vec2 cssPx = aCenter + aCorner * halfExtentCss;
  vec2 devPx = cssPx * uDpr;
  vec2 ndc = (devPx / uResolution) * 2.0 - 1.0;
  ndc.y = -ndc.y; // CSS top-left \u2192 GL bottom-left
  gl_Position = vec4(ndc, 0.0, 1.0);
}
`,_t=`#version 300 es
precision highp float;

in vec2 vCornerDev;
in vec3 vColor;
in float vHaloAlpha;
in float vCoreAlpha;
in float vHaloRadiusDev;
in float vCoreRadiusDev;

out vec4 outColor;

void main() {
  float dist = length(vCornerDev);

  // HALO: radial falloff 1 \u2192 0 from center to haloRadius.
  // Canvas2D stop 0 \u2192 haloAlpha, stop 1 \u2192 0; linear in between.
  float haloContrib = 0.0;
  if (vHaloRadiusDev > 0.0) {
    float t = clamp(dist / vHaloRadiusDev, 0.0, 1.0);
    haloContrib = vHaloAlpha * (1.0 - t);
  }

  // CORE: analytic filled circle (max(0.6, radius) CSS px \u2192 device px).
  float coreCov = clamp(vCoreRadiusDev - dist + 0.5, 0.0, 1.0);
  float coreContrib = vCoreAlpha * coreCov;

  // Both are additive; sum contributions before the additive blend.
  float totalAlpha = haloContrib + coreContrib;

  // Premultiplied additive output (blendFunc(ONE, ONE)).
  outColor = vec4(vColor * totalAlpha, totalAlpha);
}
`,zt=`#version 300 es
precision highp float;

in vec3 aPosition;     // model-space xyz (from _3dLobe)
in float aRadiusBase;  // base nodeRadius (hub?6.5 : 2.6+min(3.4,deg*0.42))
in float aHub;         // 1 = hub, 0 = non-hub
in float aStatus;      // 0=active, 1=dormantRelevant, 2=archived
in float aLobeIndex;   // lobe index 0-5
in vec3 aColor;        // node color rgb [0,1]
in float aNodeIndex;   // node-buffer index (focus/hover match)
in vec2 aCorner;       // quad corner offset in [-1, 1]^2

uniform vec2 uResolution;  // device-px framebuffer size (w, h)
uniform float uDpr;        // device pixel ratio
uniform float uRotX;
uniform float uRotY;
uniform float uSceneScale; // min(w,h) * 0.32 * zoom
uniform float uCx;
uniform float uCy;
uniform float uDist;       // 3.4
uniform float uHemisphere; // +1.0 = far pass (z>0), -1.0 = near pass (z<=0)
uniform float uHalo;       // graph.CHAOS.halo
uniform float uBloom;      // graph.CHAOS.bloom
uniform float uLobeMul[6]; // lobeVisibilityMultiplier per lobe
uniform float uFocusNodeIndex; // node index of focus node, or -1
uniform float uHoverNodeIndex; // node index of hover node, or -1

out vec2 vLocalDev;     // fragment offset from node center, in device px
out float vAlpha;       // per-node straight alpha
out float vRadiusDev;   // node radius in device px
out float vHaloRadiusDev; // halo radius in device px
flat out float vHub;    // hub flag (1/0)
flat out vec3 vColor;   // node color
flat out float vBloom;  // CHAOS.bloom

void main() {
  float cosY = cos(uRotY);
  float sinY = sin(uRotY);
  float cosX = cos(uRotX);
  float sinX = sin(uRotX);

  float rotatedX = aPosition.x * cosY + aPosition.z * sinY;
  float z1 = -aPosition.x * sinY + aPosition.z * cosY;
  float rotatedY = aPosition.y * cosX - z1 * sinX;
  float z2 = aPosition.y * sinX + z1 * cosX;

  float f = uSceneScale / (uDist + z2);
  float sx = uCx + rotatedX * f * uDist;          // CSS px
  float sy = uCy - rotatedY * f * uDist;          // CSS px
  float prScale = uDist / (uDist + z2);
  float depth = (z2 + 1.5) / 3.0;

  // far = projected z > 0 (matches drawScene's nodeProjs.filter(n=>n.z>0)).
  bool far = z2 > 0.0;
  bool wantFar = uHemisphere > 0.0;
  if (far != wantFar) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0); // off-screen cull
    vLocalDev = vec2(0.0);
    vAlpha = 0.0;
    vRadiusDev = 0.0;
    vHaloRadiusDev = 0.0;
    vHub = 0.0;
    vColor = vec3(0.0);
    vBloom = 0.0;
    return;
  }

  // Hover/focus radius bump (matches drawNode).
  float nIdx = aNodeIndex;
  bool isHover = uHoverNodeIndex >= 0.0 && abs(nIdx - uHoverNodeIndex) < 0.5;
  bool isFocus = uFocusNodeIndex >= 0.0 && abs(nIdx - uFocusNodeIndex) < 0.5;
  float bump = isHover ? 1.18 : (isFocus ? 1.25 : 1.0);

  // radius = nodeRadius(node) * max(0.55, pr.scale) * bump  (CSS px)
  float radiusCss = aRadiusBase * max(0.55, prScale) * bump;

  // fade / dim / alpha (drawNode).
  float fade = max(0.32, 1.0 - depth * 0.75);
  float dim = aStatus > 1.5 ? 0.30 : (aStatus > 0.5 ? 0.55 : 1.0); // archived/dormant/active
  int lobe = int(aLobeIndex + 0.5);
  float alpha = fade * dim * uLobeMul[lobe];

  if (alpha < 0.05) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0); // alpha-cull
    vLocalDev = vec2(0.0);
    vAlpha = 0.0;
    vRadiusDev = 0.0;
    vHaloRadiusDev = 0.0;
    vHub = 0.0;
    vColor = vec3(0.0);
    vBloom = 0.0;
    return;
  }

  // Bounding half-extent in CSS px: max of halo, ring outer, crosshair arm.
  // Stroke half-width 0.4 (lineWidth 0.8) + ~1 CSS px AA pad.
  float haloRadiusCss = radiusCss * 3.6 * uHalo;
  float strokePad = 0.4 + 1.0;
  float ringOuterCss = radiusCss + 4.0 + strokePad;
  float crosshairCss = radiusCss * 3.2 + strokePad;
  float boundCss = haloRadiusCss;
  if (aHub > 0.5) {
    boundCss = max(boundCss, max(ringOuterCss, crosshairCss));
  }
  // Guard against a zero bound (halo=0 + non-hub): keep at least the core+dot.
  boundCss = max(boundCss, radiusCss + 1.0);

  vAlpha = alpha;
  vRadiusDev = radiusCss * uDpr;
  vHaloRadiusDev = haloRadiusCss * uDpr;
  vHub = aHub;
  vColor = aColor;
  vBloom = uBloom;
  vLocalDev = aCorner * boundCss * uDpr;

  // Place quad corner at screen(sx,sy) + corner*boundCss (CSS px), then to clip.
  vec2 cssPx = vec2(sx, sy) + aCorner * boundCss;
  vec2 devPx = cssPx * uDpr;
  vec2 ndc = (devPx / uResolution) * 2.0 - 1.0;
  ndc.y = -ndc.y;
  gl_Position = vec4(ndc, 0.0, 1.0);
}
`,Vt=`#version 300 es
precision highp float;

uniform float uDpr;    // device pixel ratio (CSS\u2192device px scale for layer geometry)

in vec2 vLocalDev;     // fragment offset from node center (device px)
in float vAlpha;       // per-node straight alpha
in float vRadiusDev;   // node radius (device px)
in float vHaloRadiusDev; // halo radius (device px)
flat in float vHub;
flat in vec3 vColor;
flat in float vBloom;

out vec4 outColor;

// Source-over a straight-color layer (premultiplied) onto a premultiplied
// accumulator: acc = layerPremult + acc*(1 - layerAlpha).
vec4 over(vec4 acc, vec3 color, float layerAlpha) {
  vec3 layerPremult = color * layerAlpha;
  return vec4(layerPremult + acc.rgb * (1.0 - layerAlpha),
              layerAlpha + acc.a * (1.0 - layerAlpha));
}

void main() {
  float dist = length(vLocalDev);          // device px from node center
  float lx = vLocalDev.x;
  float ly = vLocalDev.y;

  // Accumulator starts transparent (premultiplied rgba = 0).
  vec4 acc = vec4(0.0);

  // ---- HALO (bottom): radial gradient c@0 \u2192 0@1, source-over ----
  // Canvas2D fills a haloRadius circle whose alpha falls 1\u21920 linearly with t.
  if (vHaloRadiusDev > 0.0) {
    float t = clamp(dist / vHaloRadiusDev, 0.0, 1.0);
    float haloA = 0.32 * vAlpha * vBloom * (1.0 - t);
    acc = over(acc, vColor, haloA);
  }

  // ---- CORE: filled circle of the node radius, color node.color ----
  float coreCov = clamp(vRadiusDev - dist + 0.5, 0.0, 1.0);
  float coreA = min(1.0, vAlpha * 0.93) * coreCov;
  acc = over(acc, vColor, coreA);

  // ---- WHITE DOT: filled circle radius max(0.7, radius*0.42), white ----
  // max(0.7, radius*0.42) is in CSS px; 0.7 CSS px \u2192 0.7*uDpr device px.
  float dotRadiusDev = max(0.7 * uDpr, vRadiusDev * 0.42);
  float dotCov = clamp(dotRadiusDev - dist + 0.5, 0.0, 1.0);
  float dotA = min(1.0, vAlpha) * dotCov;
  acc = over(acc, vec3(1.0), dotA);

  if (vHub > 0.5) {
    // Stroke half-width 0.4 CSS px \u2192 device px.
    float halfStrokeDev = 0.4 * uDpr;

    // ---- HUB RING: stroked circle radius radius+4, lineWidth 0.8 ----
    float ringRadiusDev = vRadiusDev + 4.0 * uDpr;
    float ringDist = abs(dist - ringRadiusDev);
    float ringCov = clamp(halfStrokeDev - ringDist + 0.5, 0.0, 1.0);
    float ringA = min(1.0, 0.55 * vAlpha) * ringCov;
    acc = over(acc, vColor, ringA);

    // ---- HUB CROSSHAIR: two lines through center, half-length radius*3.2 ----
    float armDev = vRadiusDev * 3.2;
    // Horizontal arm: |ly| within halfStroke AND |lx| <= armDev.
    float hCov = clamp(halfStrokeDev - abs(ly) + 0.5, 0.0, 1.0)
               * clamp(armDev - abs(lx) + 0.5, 0.0, 1.0);
    // Vertical arm: |lx| within halfStroke AND |ly| <= armDev.
    float vCov = clamp(halfStrokeDev - abs(lx) + 0.5, 0.0, 1.0)
               * clamp(armDev - abs(ly) + 0.5, 0.0, 1.0);
    float crossCov = max(hCov, vCov);
    float crossA = min(1.0, 0.45 * vAlpha) * crossCov;
    acc = over(acc, vColor, crossA);
  }

  // acc is already premultiplied. Output for blendFunc(ONE, ONE_MINUS_SRC_ALPHA).
  outColor = acc;
}
`;var re=26,ne=72;function br(){let t=new Uint32Array(ne),r=0;for(let e=0;e<12;e++){let o=2*e,i=2*e+1,n=2*e+2,a=2*e+3;t[r++]=o,t[r++]=i,t[r++]=a,t[r++]=o,t[r++]=a,t[r++]=n}return t}var Ht=12,ue=Ht+1,Gt=2;function ge(t,r,e){let o=e!=null?e:{positions:new Float32Array(re*3),tangentRef:new Float32Array(re*3),segStartRef:new Float32Array(re*3)},i=(t.x+r.x)*.35,n=(t.y+r.y)*.35,a=(t.z+r.z)*.35,c=new Float64Array(ue),l=new Float64Array(ue),s=new Float64Array(ue);for(let b=0;b<ue;b++){let m=b/Ht,g=1-m;c[b]=g*g*t.x+2*g*m*i+m*m*r.x,l[b]=g*g*t.y+2*g*m*n+m*m*r.y,s[b]=g*g*t.z+2*g*m*a+m*m*r.z}let{positions:u,tangentRef:f,segStartRef:d}=o;for(let b=0;b<ue;b++){let m=c[b],g=l[b],x=s[b],v=b<ue-1?b+1:b-1,h=b>0?b-1:0;for(let p=0;p<Gt;p++){let y=b*Gt+p;u[y*3+0]=m,u[y*3+1]=g,u[y*3+2]=x,f[y*3+0]=c[v],f[y*3+1]=l[v],f[y*3+2]=s[v],d[y*3+0]=c[h],d[y*3+1]=l[h],d[y*3+2]=s[h]}}return o}var ie={frontal:0,parietal:1,temporal:2,occipital:3,cerebellum:4,stem:5},gr={frontal:"project",parietal:"concept",temporal:"person",occipital:"source",cerebellum:"dailyNote",stem:"index"};function Kt(t,r){var i;let e=gr[t],o=(i=r.activePalette.kinds[e])!=null?i:r.activePalette.hud;return W(o)}function vr(t){return t.hub?6.5:2.6+Math.min(3.4,(t.degree||0)*.42)}function xr(t){return t==="dormantRelevant"?1:t==="archived"?2:0}function Ut(t){var w,T,O,X,q,_;let n=new Map,a=0;for(let I of t.nodes)I._3dLobe&&n.set(I.id,a++);let c=[];for(let I=0;I<t.edges.length;I++){let H=t.edges[I],U=t.idx[H.a],$=t.idx[H.b];!(U!=null&&U._3dLobe)||!($!=null&&$._3dLobe)||c.push({edgeIdx:I,A:U,B:$})}let l=c.length*26,s=new Float32Array(l*3),u=new Float32Array(l*3),f=new Float32Array(l*3),d=new Float32Array(l),b=new Float32Array(l*3),m=new Float32Array(l*3),g=new Float32Array(l*3),x=new Uint8Array(l),v=new Uint8Array(l),h=new Uint8Array(l),p=new Uint32Array(l),y=new Uint32Array(l),C=new Uint8Array(l),L=new Uint8Array(l),A=new Uint32Array(l),R=[],B=new Uint32Array(c.length*ne),P=br(),N=ge({x:0,y:0,z:0},{x:0,y:0,z:0}),D=0;for(let I=0;I<c.length;I++){let{edgeIdx:H,A:U,B:$}=c[I],ke=(w=U._lobeName)!=null?w:"parietal",Oe=(T=$._lobeName)!=null?T:"parietal",at=ke===Oe?1:0,_e=Kt(ke,t),ze=Kt(Oe,t),Ve=W(U.color),eo=(O=ie[ke])!=null?O:0,to=(X=ie[Oe])!=null?X:0,oo=(q=n.get(U.id))!=null?q:0,ro=(_=n.get($.id))!=null?_:0;ge(U._3dLobe,$._3dLobe,N);let Ge=N.positions,Ke=N.tangentRef,He=N.segStartRef;for(let G=0;G<13;G++){let io=Math.max(0,Math.min(G-1,11)),ao=at===0&&G>6?1:0;for(let ye=0;ye<2;ye++){let so=ye===0?-1:1,K=G*2+ye,S=D+K;s[S*3+0]=Ge[K*3+0],s[S*3+1]=Ge[K*3+1],s[S*3+2]=Ge[K*3+2],u[S*3+0]=Ke[K*3+0],u[S*3+1]=Ke[K*3+1],u[S*3+2]=Ke[K*3+2],f[S*3+0]=He[K*3+0],f[S*3+1]=He[K*3+1],f[S*3+2]=He[K*3+2],d[S]=so,b[S*3+0]=_e[0],b[S*3+1]=_e[1],b[S*3+2]=_e[2],m[S*3+0]=ze[0],m[S*3+1]=ze[1],m[S*3+2]=ze[2],g[S*3+0]=Ve[0],g[S*3+1]=Ve[1],g[S*3+2]=Ve[2],x[S]=at,v[S]=ao,h[S]=io,p[S]=oo,y[S]=ro,C[S]=eo,L[S]=to,A[S]=I}}let no=I*ne;for(let G=0;G<ne;G++)B[no+G]=D+P[G];R.push({edgeIndex:H,start:D,count:26}),D+=26}return{positions:s,tangentRef:u,segStartRef:f,sides:d,colorA:b,colorB:m,focusColor:g,sameLobe:x,colorSelector:v,segmentIndex:h,nodeIdxA:p,nodeIdxB:y,lobeIdxA:C,lobeIdxB:L,edgeIndex:A,indices:B,vertexCount:l,edgeRanges:R}}function Yt(t){var a,c,l,s;let r=t.length,e=new Float32Array(r*3),o=new Uint8Array(r),i=new Float32Array(r),n=new Float32Array(r);for(let u=0;u<r;u++){let f=t[u];e[u*3+0]=f.x,e[u*3+1]=f.y,e[u*3+2]=f.z;let d=(a=f.lobe)!=null?a:"parietal";o[u]=(c=ie[d])!=null?c:1,i[u]=(l=f.twPhase)!=null?l:0,n[u]=(s=f.twFreq)!=null?s:1}return{positions:e,lobeIndex:o,phase:i,freq:n,count:r}}function jt(t){var u,f;let r=t.filter(d=>!!d._3dLobe),e=r.length,o=new Float32Array(e*3),i=new Float32Array(e),n=new Uint8Array(e),a=new Uint8Array(e),c=new Uint8Array(e),l=new Float32Array(e*3),s=new Uint32Array(e);for(let d=0;d<e;d++){let b=r[d],m=(u=b._lobeName)!=null?u:"parietal";o[d*3+0]=b._3dLobe.x,o[d*3+1]=b._3dLobe.y,o[d*3+2]=b._3dLobe.z,i[d]=vr(b),n[d]=b.hub?1:0,a[d]=xr(b.status),c[d]=(f=ie[m])!=null?f:1;let g=W(b.color);l[d*3+0]=g[0],l[d*3+1]=g[1],l[d*3+2]=g[2],s[d]=d}return{positions:o,radius:i,hub:n,status:a,lobeIndex:c,color:l,nodeIndex:s,count:e}}function Wt(t,r){let e=new Map,o=0;for(let n of t.nodes)n._3dLobe&&e.set(n.id,o++);let i=new Map;for(let n=0;n<r.length;n++){let a=r[n],c=t.edges[a.edgeIndex];if(!c)continue;let l=t.idx[c.a],s=t.idx[c.b];if(!(l!=null&&l._3dLobe)||!(s!=null&&s._3dLobe))continue;let u=e.get(l.id),f=e.get(s.id);u!==void 0&&(i.has(u)||i.set(u,[]),i.get(u).push({start:a.start,count:a.count})),f!==void 0&&(i.has(f)||i.set(f,[]),i.get(f).push({start:a.start,count:a.count}))}return i}var yr=1e4,Lr=(()=>{let t=new Array(6);for(let r in ie)t[ie[r]]=r;return t})();function Cr(t,r,e){let o=t.replace("#",""),i=r.replace("#",""),n=parseInt(o.slice(0,2),16),a=parseInt(o.slice(2,4),16),c=parseInt(o.slice(4,6),16),l=parseInt(i.slice(0,2),16),s=parseInt(i.slice(2,4),16),u=parseInt(i.slice(4,6),16);return[Math.round(n+(l-n)*e)/255,Math.round(a+(s-a)*e)/255,Math.round(c+(u-c)*e)/255]}var Xt=64,qt=25,ot=0,rt=3,nt=6,$t=13,it=6,Zt=[[-1,-1],[1,-1],[-1,1],[-1,1],[1,-1],[1,1]],ae=class extends ce{constructor(){super(...arguments);this.gl=null;this.overlay=null;this.overlayCtx=null;this.bgProgram=null;this.hazeProgram=null;this.cloudProgram=null;this.edgeProgram=null;this.edgeGraph=null;this.nodeProgram=null;this.nodeGraph=null;this.signalProgram=null;this.nodeUploadScratch=new Float32Array(it*$t);this.contextLost=!1;this.contextLostTimer=null;this.unavailableCalled=!1;this.onContextLost=e=>{e.preventDefault(),this.contextLost=!0,this.raf!=null&&(window.cancelAnimationFrame(this.raf),this.raf=null),this.frameTimeout!=null&&(window.clearTimeout(this.frameTimeout),this.frameTimeout=null),this.contextLostTimer!=null&&window.clearTimeout(this.contextLostTimer),this.contextLostTimer=window.setTimeout(()=>{this.contextLostTimer=null,this.contextLost&&this.callUnavailable()},yr)};this.onContextRestored=()=>{this.contextLostTimer!=null&&(window.clearTimeout(this.contextLostTimer),this.contextLostTimer=null),this.bgProgram=null,this.hazeProgram=null,this.cloudProgram=null,this.edgeProgram=null,this.edgeGraph=null,this.nodeProgram=null,this.nodeGraph=null,this.signalProgram=null,this.contextLost=!1;try{this.gl&&this.canvas&&this.resizeSurface(),this.requestImmediateFrame()}catch(e){this.callUnavailable()}}}callUnavailable(){var e,o;this.unavailableCalled||(this.unavailableCalled=!0,(o=(e=this.options).onRendererUnavailable)==null||o.call(e))}acquireSurface(e){let o=e.getContext("webgl2",{alpha:!1,antialias:!1,premultipliedAlpha:!0});if(!o)return!1;this.gl=o,this.unavailableCalled=!1,this.contextLost=!1,e.addEventListener("webglcontextlost",this.onContextLost),e.addEventListener("webglcontextrestored",this.onContextRestored);let i=e.ownerDocument.createElement("canvas");i.classList.add("brain-atlas-gl-overlay");let n=e.parentElement;return n&&n.appendChild(i),this.overlay=i,this.overlayCtx=i.getContext("2d"),!0}isReady(){return!!this.gl&&!this.contextLost}getOverlayCanvasForTest(){return this.overlay}loseContextForTest(){var o;let e=(o=this.gl)==null?void 0:o.getExtension("WEBGL_lose_context");e==null||e.loseContext()}restoreContextForTest(){var o;let e=(o=this.gl)==null?void 0:o.getExtension("WEBGL_lose_context");e==null||e.restoreContext()}isContextLostForTest(){return this.contextLost}resizeSurface(){let e=this.gl;if(!this.canvas||!e)return;let o=Math.floor(this.width*this.dpr),i=Math.floor(this.height*this.dpr);this.canvas.width=o,this.canvas.height=i,this.canvas.style.width=`${this.width}px`,this.canvas.style.height=`${this.height}px`,e.viewport(0,0,o,i),this.overlay&&(this.overlay.width=o,this.overlay.height=i,this.overlay.style.width=`${this.width}px`,this.overlay.style.height=`${this.height}px`),this.overlayCtx&&this.overlayCtx.setTransform(this.dpr,0,0,this.dpr,0,0)}releaseSurface(){this.canvas&&(this.canvas.removeEventListener("webglcontextlost",this.onContextLost),this.canvas.removeEventListener("webglcontextrestored",this.onContextRestored)),this.contextLostTimer!=null&&(window.clearTimeout(this.contextLostTimer),this.contextLostTimer=null);let e=this.gl;e&&!this.contextLost&&(this.bgProgram&&(e.deleteVertexArray(this.bgProgram.vao),e.deleteBuffer(this.bgProgram.quadBuffer),e.deleteProgram(this.bgProgram.program)),this.hazeProgram&&(e.deleteVertexArray(this.hazeProgram.vao),e.deleteBuffer(this.hazeProgram.quadBuffer),e.deleteProgram(this.hazeProgram.program)),this.cloudProgram&&(e.deleteVertexArray(this.cloudProgram.vao),e.deleteBuffer(this.cloudProgram.vertexBuffer),e.deleteProgram(this.cloudProgram.program)),this.edgeProgram&&(e.deleteVertexArray(this.edgeProgram.vao),e.deleteBuffer(this.edgeProgram.vertexBuffer),e.deleteBuffer(this.edgeProgram.indexBuffer),e.deleteProgram(this.edgeProgram.program)),this.nodeProgram&&(e.deleteVertexArray(this.nodeProgram.vao),e.deleteBuffer(this.nodeProgram.vertexBuffer),e.deleteBuffer(this.nodeProgram.indexBuffer),e.deleteProgram(this.nodeProgram.program)),this.signalProgram&&(e.deleteVertexArray(this.signalProgram.vao),e.deleteBuffer(this.signalProgram.vertexBuffer),e.deleteProgram(this.signalProgram.program))),this.bgProgram=null,this.hazeProgram=null,this.cloudProgram=null,this.edgeProgram=null,this.edgeGraph=null,this.nodeProgram=null,this.nodeGraph=null,this.signalProgram=null,this.overlay&&this.overlay.parentElement&&this.overlay.parentElement.removeChild(this.overlay),this.overlay=null,this.overlayCtx=null,this.gl=null,this.contextLost=!1}drawScene(e){var f;let o=this.gl,i=(f=this.getGraph)==null?void 0:f.call(this);if(!o||!i||this.contextLost||o.isContextLost())return;let n=St(this.width,this.height,this.zoom,this.rot);this.overlayCtx&&this.overlayCtx.clearRect(0,0,this.width,this.height);let a=i.edges.filter(d=>{let b=i.idx[d.a],m=i.idx[d.b];return b&&m&&b._lobeName!==m._lobeName});this.spawnSignals(e,i,a),this.passEnabled("background")&&this.drawBackground(o,i,n.cx,n.cy),this.passEnabled("haze")&&this.drawHaze(o,i,n);let c=new Float32Array(6),l=new Float32Array(18);for(let d=0;d<6;d++){let b=Lr[d];c[d]=Z(b,this.options.enabledLobes,this.highlightLobe);let[m,g,x]=W(this.lobeColor(b,i));l[d*3+0]=m,l[d*3+1]=g,l[d*3+2]=x}let s=this.nodeBufferIndexOf(i,this.focusId),u=this.nodeBufferIndexOf(i,this.hoverId);if(this.passEnabled("cloud")&&this.drawCloud(o,n,e,1,c,l),this.passEnabled("edges")&&this.drawEdges(o,i,n,1,c,s,u),this.passEnabled("nodes")&&this.drawNodes(o,i,n,1,c,s,u),this.passEnabled("cloud")&&this.drawCloud(o,n,e,-1,c,l),this.passEnabled("edges")&&this.drawEdges(o,i,n,-1,c,s,u),this.passEnabled("nodes")&&this.drawNodes(o,i,n,-1,c,s,u),this.passEnabled("signals")&&this.drawSignals(o,n,e),this.passEnabled("labels")&&this.overlayCtx&&this.options.showLobeLabels){let d=this.overlayCtx,b=v=>Ie(n,v),m=this.getLobeStats(),g=v=>Z(v,this.options.enabledLobes,this.highlightLobe),x=Object.values(this.projCache);Be(d,b,i,m,g,v=>this.lobeColor(v,i)),De(d,x,i,g,{hoverId:this.hoverId,focusId:this.focusId,zoom:this.zoom,width:this.width,mobile:this.effectivePerformancePreset()==="mobile"})}this.passEnabled("compass")&&this.overlayCtx&&Me(this.overlayCtx,this.rot,i,this.width,this.height)}ensureBackgroundProgram(e){if(this.bgProgram)return this.bgProgram;let o=te(e,wt,Bt),i=e.getAttribLocation(o,"aPosition"),n=new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),a=de(e,n),c=e.createVertexArray();if(!c)throw new Error("Brain Atlas: failed to create background VAO.");e.bindVertexArray(c),e.bindBuffer(e.ARRAY_BUFFER,a),e.enableVertexAttribArray(i),e.vertexAttribPointer(i,2,e.FLOAT,!1,0,0),e.bindVertexArray(null);let l=oe(e,o,["uResolution","uDpr","uCenter","uRadius","uBg","uBgFar"]);return this.bgProgram={program:o,quadBuffer:a,vao:c,uniforms:l},this.bgProgram}drawBackground(e,o,i,n){let a=this.ensureBackgroundProgram(e),c=o.activePalette,[l,s,u]=W(c.bg),[f,d,b]=W(c.bgFar),m=Math.max(this.width,this.height)*.75;e.disable(e.BLEND),e.useProgram(a.program),e.bindVertexArray(a.vao),e.uniform2f(a.uniforms.uResolution,Math.floor(this.width*this.dpr),Math.floor(this.height*this.dpr)),e.uniform1f(a.uniforms.uDpr,this.dpr),e.uniform2f(a.uniforms.uCenter,i,n),e.uniform1f(a.uniforms.uRadius,m),e.uniform3f(a.uniforms.uBg,l,s,u),e.uniform3f(a.uniforms.uBgFar,f,d,b),e.drawArrays(e.TRIANGLES,0,6),e.bindVertexArray(null)}ensureHazeProgram(e){if(this.hazeProgram)return this.hazeProgram;let o=te(e,Dt,Mt),i=e.getAttribLocation(o,"aPosition"),n=new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),a=de(e,n),c=e.createVertexArray();if(!c)throw new Error("Brain Atlas: failed to create haze VAO.");e.bindVertexArray(c),e.bindBuffer(e.ARRAY_BUFFER,a),e.enableVertexAttribArray(i),e.vertexAttribPointer(i,2,e.FLOAT,!1,0,0),e.bindVertexArray(null);let l=oe(e,o,["uResolution","uDpr","uCenter","uRadius","uColor","uBaseA"]);return this.hazeProgram={program:o,quadBuffer:a,vao:c,uniforms:l},this.hazeProgram}drawHaze(e,o,i){let n=this.ensureHazeProgram(e);e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE),e.useProgram(n.program),e.bindVertexArray(n.vao);let a=Math.floor(this.width*this.dpr),c=Math.floor(this.height*this.dpr);e.uniform2f(n.uniforms.uResolution,a,c),e.uniform1f(n.uniforms.uDpr,this.dpr);let l=i.scale;for(let s in M){let u=s,f=M[u],d=[f.c];f.mirror&&d.push({x:-f.c.x,y:f.c.y,z:f.c.z});for(let b of d){let m=Ie(i,b),g=f.r*l*1.4*m.scale,x=Math.max(.25,1-m.depth*.55),h=(this.highlightLobe===u?.18:.07)*x*Z(u,this.options.enabledLobes,this.highlightLobe);if(h<.005)continue;let[p,y,C]=W(this.lobeColor(u,o));e.uniform2f(n.uniforms.uCenter,m.sx,m.sy),e.uniform1f(n.uniforms.uRadius,g),e.uniform3f(n.uniforms.uColor,p,y,C),e.uniform1f(n.uniforms.uBaseA,h),e.drawArrays(e.TRIANGLES,0,6)}}e.bindVertexArray(null),e.disable(e.BLEND)}ensureCloudProgram(e){if(this.cloudProgram)return this.cloudProgram;let o=te(e,It,Ft),i=we(),n=Yt(i),a=n.count,c=8,l=6,s=[[-1,-1],[1,-1],[-1,1],[-1,1],[1,-1],[1,1]],u=a*l,f=new Float32Array(u*c),d=0;for(let L=0;L<a;L++){let A=n.positions[L*3+0],R=n.positions[L*3+1],B=n.positions[L*3+2],P=n.lobeIndex[L],N=n.phase[L],D=n.freq[L];for(let w=0;w<l;w++)f[d++]=A,f[d++]=R,f[d++]=B,f[d++]=P,f[d++]=N,f[d++]=D,f[d++]=s[w][0],f[d++]=s[w][1]}let b=de(e,f),m=e.getAttribLocation(o,"aPosition"),g=e.getAttribLocation(o,"aLobeIndex"),x=e.getAttribLocation(o,"aPhase"),v=e.getAttribLocation(o,"aFreq"),h=e.getAttribLocation(o,"aCorner"),p=e.createVertexArray();if(!p)throw new Error("Brain Atlas: failed to create cloud VAO.");e.bindVertexArray(p),e.bindBuffer(e.ARRAY_BUFFER,b);let y=c*4;e.enableVertexAttribArray(m),e.vertexAttribPointer(m,3,e.FLOAT,!1,y,0),e.enableVertexAttribArray(g),e.vertexAttribPointer(g,1,e.FLOAT,!1,y,3*4),e.enableVertexAttribArray(x),e.vertexAttribPointer(x,1,e.FLOAT,!1,y,4*4),e.enableVertexAttribArray(v),e.vertexAttribPointer(v,1,e.FLOAT,!1,y,5*4),e.enableVertexAttribArray(h),e.vertexAttribPointer(h,2,e.FLOAT,!1,y,6*4),e.bindVertexArray(null);let C=oe(e,o,["uResolution","uDpr","uRotX","uRotY","uSceneScale","uCx","uCy","uDist","uTime","uHemisphere","uLobeMul[0]","uLobeColors[0]"]);return this.cloudProgram={program:o,vertexBuffer:b,vao:p,uniforms:C,vertexCount:u},this.cloudProgram}drawCloud(e,o,i,n,a,c){let l=this.ensureCloudProgram(e);e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE),e.useProgram(l.program),e.bindVertexArray(l.vao);let s=Math.floor(this.width*this.dpr),u=Math.floor(this.height*this.dpr);e.uniform2f(l.uniforms.uResolution,s,u),e.uniform1f(l.uniforms.uDpr,this.dpr),e.uniform1f(l.uniforms.uRotX,o.rotX),e.uniform1f(l.uniforms.uRotY,o.rotY),e.uniform1f(l.uniforms.uSceneScale,o.scale),e.uniform1f(l.uniforms.uCx,o.cx),e.uniform1f(l.uniforms.uCy,o.cy),e.uniform1f(l.uniforms.uDist,o.dist),e.uniform1f(l.uniforms.uTime,i),e.uniform1f(l.uniforms.uHemisphere,n),e.uniform1fv(l.uniforms["uLobeMul[0]"],a),e.uniform3fv(l.uniforms["uLobeColors[0]"],c),e.drawArrays(e.TRIANGLES,0,l.vertexCount),e.bindVertexArray(null),e.disable(e.BLEND)}onNodeMoved(e){var u;let o=this.gl,i=(u=this.getGraph)==null?void 0:u.call(this);if(!o||!i)return;let n=this.nodeBufferIndexOf(i,e);if(n<0)return;let a=i.idx[e],c=a==null?void 0:a._3dLobe;if(!c)return;let l=this.nodeProgram;if(l&&this.nodeGraph===i&&n<l.nodeCount){l.centers[n*3+0]=c.x,l.centers[n*3+1]=c.y,l.centers[n*3+2]=c.z,l.buf.positions[n*3+0]=c.x,l.buf.positions[n*3+1]=c.y,l.buf.positions[n*3+2]=c.z;let f=$t,d=this.nodeUploadScratch,b=l.buf.radius[n],m=l.buf.hub[n],g=l.buf.status[n],x=l.buf.lobeIndex[n],v=l.buf.color[n*3+0],h=l.buf.color[n*3+1],p=l.buf.color[n*3+2],y=l.buf.nodeIndex[n],C=Zt;for(let A=0;A<it;A++){let R=A*f;d[R++]=c.x,d[R++]=c.y,d[R++]=c.z,d[R++]=b,d[R++]=m,d[R++]=g,d[R++]=x,d[R++]=v,d[R++]=h,d[R++]=p,d[R++]=y,d[R++]=C[A][0],d[R++]=C[A][1]}o.bindBuffer(o.ARRAY_BUFFER,l.vertexBuffer);let L=n*it*f*4;o.bufferSubData(o.ARRAY_BUFFER,L,d),o.bindBuffer(o.ARRAY_BUFFER,null)}let s=this.edgeProgram;if(s&&this.edgeGraph===i){let f=s.incidentMap.get(n);if(f&&f.length>0)for(let d of f)this.updateEdgeBlock(o,s,d.start)}this.requestImmediateFrame()}updateEdgeBlock(e,o,i){let n=o.buf,a=n.nodeIdxA[i],c=n.nodeIdxB[i],l=o.bufIndexToNode[a],s=o.bufIndexToNode[c],u=l==null?void 0:l._3dLobe,f=s==null?void 0:s._3dLobe;if(!u||!f)return;let d=ge(u,f,o.posBlockScratch),b=qt,m=o.edgeUploadScratch,g=i/re;for(let v=0;v<re;v++){let h=i+v;n.positions[h*3+0]=d.positions[v*3+0],n.positions[h*3+1]=d.positions[v*3+1],n.positions[h*3+2]=d.positions[v*3+2],n.tangentRef[h*3+0]=d.tangentRef[v*3+0],n.tangentRef[h*3+1]=d.tangentRef[v*3+1],n.tangentRef[h*3+2]=d.tangentRef[v*3+2],n.segStartRef[h*3+0]=d.segStartRef[v*3+0],n.segStartRef[h*3+1]=d.segStartRef[v*3+1],n.segStartRef[h*3+2]=d.segStartRef[v*3+2];let p=v*b;m[p+ot+0]=d.positions[v*3+0],m[p+ot+1]=d.positions[v*3+1],m[p+ot+2]=d.positions[v*3+2],m[p+rt+0]=d.tangentRef[v*3+0],m[p+rt+1]=d.tangentRef[v*3+1],m[p+rt+2]=d.tangentRef[v*3+2],m[p+nt+0]=d.segStartRef[v*3+0],m[p+nt+1]=d.segStartRef[v*3+1],m[p+nt+2]=d.segStartRef[v*3+2],m[p+9]=n.sides[h],m[p+10]=n.colorA[h*3+0],m[p+11]=n.colorA[h*3+1],m[p+12]=n.colorA[h*3+2],m[p+13]=n.colorB[h*3+0],m[p+14]=n.colorB[h*3+1],m[p+15]=n.colorB[h*3+2],m[p+16]=n.focusColor[h*3+0],m[p+17]=n.focusColor[h*3+1],m[p+18]=n.focusColor[h*3+2],m[p+19]=n.sameLobe[h],m[p+20]=n.colorSelector[h],m[p+21]=n.lobeIdxA[h],m[p+22]=n.lobeIdxB[h],m[p+23]=n.nodeIdxA[h],m[p+24]=n.nodeIdxB[h]}let x=o.centerline;for(let v=0;v<13;v++){let h=v*2,p=(g*13+v)*3;x[p+0]=d.positions[h*3+0],x[p+1]=d.positions[h*3+1],x[p+2]=d.positions[h*3+2]}e.bindBuffer(e.ARRAY_BUFFER,o.vertexBuffer),e.bufferSubData(e.ARRAY_BUFFER,i*b*4,m),e.bindBuffer(e.ARRAY_BUFFER,null)}nodeBufferIndexOf(e,o){if(!o)return-1;let i=0;for(let n of e.nodes)if(n._3dLobe){if(n.id===o)return i;i+=1}return-1}ensureEdgeProgram(e,o){if(this.edgeProgram&&this.edgeGraph===o)return this.edgeProgram;this.edgeProgram&&(e.deleteVertexArray(this.edgeProgram.vao),e.deleteBuffer(this.edgeProgram.vertexBuffer),e.deleteBuffer(this.edgeProgram.indexBuffer),e.deleteProgram(this.edgeProgram.program),this.edgeProgram=null);let i=te(e,Tt,kt),n=Ut(o),a=n.edgeRanges.length,c=n.vertexCount,l=25,s=new Float32Array(c*l);for(let h=0;h<c;h++){let p=h*l;s[p++]=n.positions[h*3+0],s[p++]=n.positions[h*3+1],s[p++]=n.positions[h*3+2],s[p++]=n.tangentRef[h*3+0],s[p++]=n.tangentRef[h*3+1],s[p++]=n.tangentRef[h*3+2],s[p++]=n.segStartRef[h*3+0],s[p++]=n.segStartRef[h*3+1],s[p++]=n.segStartRef[h*3+2],s[p++]=n.sides[h],s[p++]=n.colorA[h*3+0],s[p++]=n.colorA[h*3+1],s[p++]=n.colorA[h*3+2],s[p++]=n.colorB[h*3+0],s[p++]=n.colorB[h*3+1],s[p++]=n.colorB[h*3+2],s[p++]=n.focusColor[h*3+0],s[p++]=n.focusColor[h*3+1],s[p++]=n.focusColor[h*3+2],s[p++]=n.sameLobe[h],s[p++]=n.colorSelector[h],s[p++]=n.lobeIdxA[h],s[p++]=n.lobeIdxB[h],s[p++]=n.nodeIdxA[h],s[p++]=n.nodeIdxB[h]}let u=de(e,s),f=new Float32Array(a*13*3);for(let h=0;h<a;h++){let p=n.edgeRanges[h].start;for(let y=0;y<13;y++){let C=p+y*2,L=(h*13+y)*3;f[L+0]=n.positions[C*3+0],f[L+1]=n.positions[C*3+1],f[L+2]=n.positions[C*3+2]}}let d=e.createBuffer();if(!d)throw new Error("Brain Atlas: failed to create edge index buffer.");e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,d),e.bufferData(e.ELEMENT_ARRAY_BUFFER,n.indices.byteLength,e.DYNAMIC_DRAW);let b=l*4,m=h=>e.getAttribLocation(i,h),g=e.createVertexArray();if(!g)throw new Error("Brain Atlas: failed to create edge VAO.");e.bindVertexArray(g),e.bindBuffer(e.ARRAY_BUFFER,u);let x=(h,p,y)=>{let C=m(h);C<0||(e.enableVertexAttribArray(C),e.vertexAttribPointer(C,p,e.FLOAT,!1,b,y*4))};x("aPosition",3,0),x("aTangentRef",3,3),x("aSegStartRef",3,6),x("aSide",1,9),x("aColorA",3,10),x("aColorB",3,13),x("aFocusColor",3,16),x("aSameLobe",1,19),x("aColorSelector",1,20),x("aLobeIdxA",1,21),x("aLobeIdxB",1,22),x("aNodeIdxA",1,23),x("aNodeIdxB",1,24),e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,d),e.bindVertexArray(null);let v=oe(e,i,["uResolution","uDpr","uRotX","uRotY","uSceneScale","uCx","uCy","uDist","uIsFar","uFocusNodeIndex","uHoverNodeIndex","uLobeMul[0]"]);return this.edgeProgram={program:i,vertexBuffer:u,indexBuffer:d,vao:g,uniforms:v,buf:n,centerline:f,edgeCount:a,meanZ:new Float32Array(a),sortScratch:new Int32Array(a),indexScratch:new Uint32Array(n.indices.length),incidentMap:Wt(o,n.edgeRanges),bufIndexToNode:o.nodes.filter(h=>!!h._3dLobe),posBlockScratch:ge({x:0,y:0,z:0},{x:0,y:0,z:0}),edgeUploadScratch:new Float32Array(re*qt)},this.edgeGraph=o,this.edgeProgram}drawEdges(e,o,i,n,a,c,l){let s=this.ensureEdgeProgram(e,o);if(s.edgeCount===0)return;let u=Math.cos(i.rotY),f=Math.sin(i.rotY),d=Math.cos(i.rotX),b=Math.sin(i.rotX),m=s.centerline,g=s.meanZ;for(let P=0;P<s.edgeCount;P++){let N=0,D=P*13*3;for(let w=0;w<13;w++){let T=D+w*3,O=m[T+0],X=m[T+1],q=m[T+2],_=-O*f+q*u,I=X*b+_*d;N+=I}g[P]=N/13}let x=n>0,v=s.sortScratch,h=0;for(let P=0;P<s.edgeCount;P++)g[P]>0===x&&(v[h++]=P);if(h===0)return;let p=v.subarray(0,h);p.sort((P,N)=>g[N]-g[P]);let y=s.buf.indices,C=s.indexScratch,L=0;for(let P=0;P<h;P++){let D=p[P]*ne;for(let w=0;w<ne;w++)C[L++]=y[D+w]}let A=L;e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE_MINUS_SRC_ALPHA),e.useProgram(s.program),e.bindVertexArray(s.vao),e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,s.indexBuffer),e.bufferSubData(e.ELEMENT_ARRAY_BUFFER,0,C,0,A);let R=Math.floor(this.width*this.dpr),B=Math.floor(this.height*this.dpr);e.uniform2f(s.uniforms.uResolution,R,B),e.uniform1f(s.uniforms.uDpr,this.dpr),e.uniform1f(s.uniforms.uRotX,i.rotX),e.uniform1f(s.uniforms.uRotY,i.rotY),e.uniform1f(s.uniforms.uSceneScale,i.scale),e.uniform1f(s.uniforms.uCx,i.cx),e.uniform1f(s.uniforms.uCy,i.cy),e.uniform1f(s.uniforms.uDist,i.dist),e.uniform1f(s.uniforms.uIsFar,x?1:0),e.uniform1f(s.uniforms.uFocusNodeIndex,c),e.uniform1f(s.uniforms.uHoverNodeIndex,l),e.uniform1fv(s.uniforms["uLobeMul[0]"],a),e.drawElements(e.TRIANGLES,A,e.UNSIGNED_INT,0),e.bindVertexArray(null),e.disable(e.BLEND)}ensureNodeProgram(e,o){if(this.nodeProgram&&this.nodeGraph===o)return this.nodeProgram;this.nodeProgram&&(e.deleteVertexArray(this.nodeProgram.vao),e.deleteBuffer(this.nodeProgram.vertexBuffer),e.deleteBuffer(this.nodeProgram.indexBuffer),e.deleteProgram(this.nodeProgram.program),this.nodeProgram=null);let i=te(e,zt,Vt),n=jt(o.nodes),a=n.count,c=13,l=6,s=Zt,u=a*l,f=new Float32Array(u*c),d=0;for(let L=0;L<a;L++){let A=n.positions[L*3+0],R=n.positions[L*3+1],B=n.positions[L*3+2],P=n.radius[L],N=n.hub[L],D=n.status[L],w=n.lobeIndex[L],T=n.color[L*3+0],O=n.color[L*3+1],X=n.color[L*3+2],q=n.nodeIndex[L];for(let _=0;_<l;_++)f[d++]=A,f[d++]=R,f[d++]=B,f[d++]=P,f[d++]=N,f[d++]=D,f[d++]=w,f[d++]=T,f[d++]=O,f[d++]=X,f[d++]=q,f[d++]=s[_][0],f[d++]=s[_][1]}let b=de(e,f),m=new Float32Array(a*3);m.set(n.positions.subarray(0,a*3));let g=new Uint32Array(a*6);for(let L=0;L<a;L++){let A=L*l,R=L*6;g[R+0]=A+0,g[R+1]=A+1,g[R+2]=A+2,g[R+3]=A+3,g[R+4]=A+4,g[R+5]=A+5}let x=e.createBuffer();if(!x)throw new Error("Brain Atlas: failed to create node index buffer.");e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,x),e.bufferData(e.ELEMENT_ARRAY_BUFFER,g.byteLength,e.DYNAMIC_DRAW);let v=c*4,h=L=>e.getAttribLocation(i,L),p=e.createVertexArray();if(!p)throw new Error("Brain Atlas: failed to create node VAO.");e.bindVertexArray(p),e.bindBuffer(e.ARRAY_BUFFER,b);let y=(L,A,R)=>{let B=h(L);B<0||(e.enableVertexAttribArray(B),e.vertexAttribPointer(B,A,e.FLOAT,!1,v,R*4))};y("aPosition",3,0),y("aRadiusBase",1,3),y("aHub",1,4),y("aStatus",1,5),y("aLobeIndex",1,6),y("aColor",3,7),y("aNodeIndex",1,10),y("aCorner",2,11),e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,x),e.bindVertexArray(null);let C=oe(e,i,["uResolution","uDpr","uRotX","uRotY","uSceneScale","uCx","uCy","uDist","uHemisphere","uHalo","uBloom","uFocusNodeIndex","uHoverNodeIndex","uLobeMul[0]"]);return this.nodeProgram={program:i,vertexBuffer:b,indexBuffer:x,vao:p,uniforms:C,buf:n,centers:m,nodeCount:a,projZ:new Float32Array(a),sortScratch:new Int32Array(a),baseIndices:g,indexScratch:new Uint32Array(a*6)},this.nodeGraph=o,this.nodeProgram}drawNodes(e,o,i,n,a,c,l){let s=this.ensureNodeProgram(e,o);if(s.nodeCount===0)return;let u=Math.cos(i.rotY),f=Math.sin(i.rotY),d=Math.cos(i.rotX),b=Math.sin(i.rotX),m=s.centers,g=s.projZ;for(let P=0;P<s.nodeCount;P++){let N=m[P*3+0],D=m[P*3+1],w=m[P*3+2],T=-N*f+w*u,O=D*b+T*d;g[P]=O}let x=n>0,v=s.sortScratch,h=0;for(let P=0;P<s.nodeCount;P++)g[P]>0===x&&(v[h++]=P);if(h===0)return;let p=v.subarray(0,h);p.sort((P,N)=>g[N]-g[P]);let y=s.baseIndices,C=s.indexScratch,L=0;for(let P=0;P<h;P++){let D=p[P]*6;for(let w=0;w<6;w++)C[L++]=y[D+w]}let A=L;e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE_MINUS_SRC_ALPHA),e.useProgram(s.program),e.bindVertexArray(s.vao),e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,s.indexBuffer),e.bufferSubData(e.ELEMENT_ARRAY_BUFFER,0,C,0,A);let R=Math.floor(this.width*this.dpr),B=Math.floor(this.height*this.dpr);e.uniform2f(s.uniforms.uResolution,R,B),e.uniform1f(s.uniforms.uDpr,this.dpr),e.uniform1f(s.uniforms.uRotX,i.rotX),e.uniform1f(s.uniforms.uRotY,i.rotY),e.uniform1f(s.uniforms.uSceneScale,i.scale),e.uniform1f(s.uniforms.uCx,i.cx),e.uniform1f(s.uniforms.uCy,i.cy),e.uniform1f(s.uniforms.uDist,i.dist),e.uniform1f(s.uniforms.uHemisphere,x?1:-1),e.uniform1f(s.uniforms.uHalo,o.CHAOS.halo),e.uniform1f(s.uniforms.uBloom,o.CHAOS.bloom),e.uniform1f(s.uniforms.uFocusNodeIndex,c),e.uniform1f(s.uniforms.uHoverNodeIndex,l),e.uniform1fv(s.uniforms["uLobeMul[0]"],a),e.drawElements(e.TRIANGLES,A,e.UNSIGNED_INT,0),e.bindVertexArray(null),e.disable(e.BLEND)}ensureSignalProgram(e){if(this.signalProgram)return this.signalProgram;let o=te(e,Ot,_t),i=11,a=Xt*6*i,c=a*4,l=e.createBuffer();if(!l)throw new Error("Brain Atlas: failed to create signal vertex buffer.");e.bindBuffer(e.ARRAY_BUFFER,l),e.bufferData(e.ARRAY_BUFFER,c,e.DYNAMIC_DRAW);let s=i*4,u=m=>e.getAttribLocation(o,m),f=e.createVertexArray();if(!f)throw new Error("Brain Atlas: failed to create signal VAO.");e.bindVertexArray(f),e.bindBuffer(e.ARRAY_BUFFER,l);let d=(m,g,x)=>{let v=u(m);v<0||(e.enableVertexAttribArray(v),e.vertexAttribPointer(v,g,e.FLOAT,!1,s,x*4))};d("aCenter",2,0),d("aCorner",2,2),d("aColor",3,4),d("aHaloAlpha",1,7),d("aCoreAlpha",1,8),d("aHaloRadiusDev",1,9),d("aCoreRadiusDev",1,10),e.bindVertexArray(null);let b=oe(e,o,["uResolution","uDpr"]);return this.signalProgram={program:o,vertexBuffer:l,vao:f,uniforms:b,scratch:new Float32Array(a),capacityBytes:c},this.signalProgram}drawSignals(e,o,i){if(this.signals.length===0)return;let n=this.ensureSignalProgram(e),a=n.scratch,c=11,l=6,s=[[-1,-1],[1,-1],[-1,1],[-1,1],[1,-1],[1,1]],u=0,f=0;for(let m of this.signals){if(!m.a._3dLobe||!m.b._3dLobe)continue;let g=(i-m.born)/m.dur;if(g<0||g>1)continue;let x=Math.sin(g*Math.PI),v=Math.max(Z(m.a._lobeName,this.options.enabledLobes,this.highlightLobe),Z(m.b._lobeName,this.options.enabledLobes,this.highlightLobe)),h=m.a._3dLobe,p=m.b._3dLobe,y={x:(h.x+p.x)*.35,y:(h.y+p.y)*.35,z:(h.z+p.z)*.35};for(let C=0;C<6&&!(u>=Xt);C+=1){let L=Math.max(0,g-C*.035),A=1-L,R={x:A*A*h.x+2*A*L*y.x+L*L*p.x,y:A*A*h.y+2*A*L*y.y+L*L*p.y,z:A*A*h.z+2*A*L*y.z+L*L*p.z},B=Ie(o,R),[P,N,D]=Cr(m.colA,m.colB,L),w=(1-C/6)*x,T=Math.max(.3,1-B.depth*.6),O=(1.3-C*.15)*Math.max(.5,B.scale),X=.22*w*T*v,q=.55*w*T*v,_=O*3.2*this.dpr,I=Math.max(.6,O)*this.dpr;for(let H=0;H<l;H++)a[f++]=B.sx,a[f++]=B.sy,a[f++]=s[H][0],a[f++]=s[H][1],a[f++]=P,a[f++]=N,a[f++]=D,a[f++]=X,a[f++]=q,a[f++]=_,a[f++]=I;u+=1}}if(u===0)return;e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE),e.useProgram(n.program),e.bindVertexArray(n.vao),e.bindBuffer(e.ARRAY_BUFFER,n.vertexBuffer),e.bufferSubData(e.ARRAY_BUFFER,0,a,0,u*l*c);let d=Math.floor(this.width*this.dpr),b=Math.floor(this.height*this.dpr);e.uniform2f(n.uniforms.uResolution,d,b),e.uniform1f(n.uniforms.uDpr,this.dpr),e.drawArrays(e.TRIANGLES,0,u*l),e.bindVertexArray(null),e.disable(e.BLEND)}};var xe="brain-atlas",ve=class extends fe.ItemView{constructor(e,o){super(e);this.renderer=new J;this.graph=null;this.rootEl=null;this.canvas=null;this.controlsEl=null;this.legendEl=null;this.tooltipEl=null;this.focusEl=null;this.infoEl=null;this.emptyEl=null;this.infoButton=null;this.labelButton=null;this.allButton=null;this.noneButton=null;this.lobeButtons={};this.showInfo=!1;this.pendingOpenNodeId=null;this.pendingOpenAt=0;this.canvasContextKind=null;this.rendererStarted=!1;this.fallingBack=!1;this.syncOverlays=()=>{var o;let e=this.graph;e&&(this.syncControls(),this.syncLegend(e),this.syncInfoPanel(),this.syncTooltip(),this.syncFocusCard(),(o=this.emptyEl)==null||o.toggleClass("is-visible",e.nodes.length===0))};this.onCanvasClick=e=>{var a;if(!this.canvas||this.renderer.consumeSuppressedClick())return;let i=((a=this.renderer.getInteractionTarget())!=null?a:this.canvas).getBoundingClientRect(),n=this.renderer.hitTest(e.clientX-i.left,e.clientY-i.top);n&&(this.shouldPreviewBeforeOpen(n)||(this.pendingOpenNodeId=null,this.openNode(n)))};this.plugin=o}getViewType(){return xe}getDisplayText(){return"Brain Atlas"}getIcon(){return"brain"}async onOpen(){this.contentEl.empty(),this.contentEl.addClass("brain-atlas-view");let e=this.contentEl.createDiv({cls:"brain-atlas-root"});this.rootEl=e,this.syncPaletteClass(),this.canvas=e.createEl("canvas",{cls:"brain-atlas-canvas"}),this.createHud(e),this.createControls(e),this.legendEl=e.createDiv({cls:"brain-atlas-legend"}),this.infoEl=e.createDiv({cls:"brain-atlas-info-panel"}),this.tooltipEl=e.createDiv({cls:"brain-atlas-tooltip"}),this.focusEl=e.createDiv({cls:"brain-atlas-focus-card"}),this.emptyEl=e.createDiv({cls:"brain-atlas-empty"}),this.emptyEl.setText("Your brain is empty. Add notes with #project, #person, or #source tags to start mapping."),this.canvas.addEventListener("click",this.onCanvasClick),this.rebuild()}async onClose(){var e;(e=this.canvas)==null||e.removeEventListener("click",this.onCanvasClick),this.renderer.stop(),this.rendererStarted=!1,this.rootEl=null,this.canvas=null,this.canvasContextKind=null,this.graph=null}onShow(){this.canvas&&this.graph&&this.startRenderer()}onHide(){this.renderer.stop(),this.rendererStarted=!1}rebuild(){this.graph=yt(this.plugin.app,this.plugin.settings),this.syncPaletteClass();let e=this.plugin.settings.rendererMode==="webgl2"||this.plugin.settings.rendererMode==="auto"&&!this.isMobileRuntime(),o=this.renderer instanceof ae;!this.rendererStarted||e!==o?this.startRenderer():this.renderer.setOptions(this.rendererOptions()),this.syncOverlays()}rendererOptions(){return{idleAutoRotate:this.plugin.settings.idleAutoRotate,showLobeLabels:this.plugin.settings.showLobeLabels,enabledLobes:this.plugin.settings.enabledLobes,performancePreset:this.plugin.settings.performancePreset,mobileMode:this.isMobileRuntime(),onPinNode:(e,o)=>this.pinNode(e,o),onChange:this.syncOverlays,onRendererUnavailable:()=>this.fallbackToCanvas2D()}}selectRenderer(){let e=this.plugin.settings.rendererMode;return e==="canvas2d"?new J:e==="webgl2"||e==="auto"&&!this.isMobileRuntime()?new ae:new J}fallbackToCanvas2D(){if(!this.fallingBack&&this.renderer instanceof ae&&!(!this.canvas||!this.rootEl)){this.fallingBack=!0;try{this.renderer.stop(),this.rendererStarted=!1,this.recreateCanvas();let e=()=>{var n;return(n=this.graph)!=null?n:Jt(this.plugin.settings)},o=this.rendererOptions(),i=new J;try{i.start(this.canvas,e,o),this.renderer=i,this.canvasContextKind="2d",this.rendererStarted=!0}catch(n){this.showNoRendererError()}}finally{this.fallingBack=!1}}}showNoRendererError(){this.emptyEl&&(this.emptyEl.setText("Brain Atlas couldn\u2019t start a renderer (WebGL2 and Canvas2D both unavailable)."),this.emptyEl.addClass("is-visible"))}recreateCanvas(){var o,i;if(!this.rootEl)return;(o=this.canvas)==null||o.removeEventListener("click",this.onCanvasClick),(i=this.canvas)==null||i.remove();let e=this.rootEl.createEl("canvas",{cls:"brain-atlas-canvas"});this.rootEl.prepend(e),e.addEventListener("click",this.onCanvasClick),this.canvas=e,this.canvasContextKind=null}startRenderer(){if(!this.canvas||!this.rootEl)return;let e=()=>{var c;return(c=this.graph)!=null?c:Jt(this.plugin.settings)},o=this.rendererOptions();this.renderer.stop(),this.rendererStarted=!1;let i=this.selectRenderer(),n=i instanceof ae?"webgl2":"2d";this.canvasContextKind!==null&&this.canvasContextKind!==n&&this.recreateCanvas();let a=this.canvas;try{i.start(a,e,o),this.renderer=i,this.canvasContextKind=n,this.rendererStarted=!0}catch(c){let l=new J;try{l.start(a,e,o),this.renderer=l,this.canvasContextKind="2d",this.rendererStarted=!0}catch(s){this.recreateCanvas();try{l.start(this.canvas,e,o),this.renderer=l,this.canvasContextKind="2d",this.rendererStarted=!0}catch(u){this.showNoRendererError()}}}}isMobileRuntime(){return fe.Platform.isMobile?!0:typeof window=="undefined"?!1:window.innerWidth<=700||typeof window.matchMedia=="function"&&window.matchMedia("(pointer: coarse)").matches}createHud(e){let o=e.createDiv({cls:"brain-atlas-hud"});o.createSpan({cls:"brain-atlas-pulse"}),o.createSpan({text:"LOBE - ATLAS - v2"}),o.createSpan({cls:"brain-atlas-muted",text:" -"}),o.createSpan({text:" 6 regions"}),e.createDiv({cls:"brain-atlas-help"}).setText("DRAG NODE - pin   -   DRAG EMPTY - rotate   -   SCROLL - zoom")}createControls(e){var n;this.controlsEl=e.createDiv({cls:"brain-atlas-controls"});let o=this.controlsEl.createDiv({cls:"brain-atlas-control-group"});this.infoButton=this.createControlButton(o,"Info",()=>this.toggleInfo()),this.labelButton=this.createControlButton(o,"Labels",()=>this.toggleLabels()),this.allButton=this.createControlButton(o,"All",()=>this.setAllRegions(!0)),this.noneButton=this.createControlButton(o,"None",()=>this.setAllRegions(!1));let i=this.controlsEl.createDiv({cls:"brain-atlas-control-group brain-atlas-region-controls"});for(let a of k)this.lobeButtons[a]=this.createControlButton(i,Rr(a),()=>this.toggleLobe(a)),(n=this.lobeButtons[a])==null||n.setAttr("aria-label",`${M[a].label} region`)}createControlButton(e,o,i){let n=e.createEl("button",{cls:"brain-atlas-control-button",text:o});return n.type="button",n.addEventListener("click",a=>{a.preventDefault(),a.stopPropagation(),i()}),n}syncPaletteClass(){var e;(e=this.rootEl)==null||e.toggleClass("is-light-palette",this.plugin.settings.palette==="daylight")}syncControls(){var i,n,a,c,l,s;let e=this.plugin.settings.enabledLobes;(i=this.infoButton)==null||i.toggleClass("is-active",this.showInfo),(n=this.infoButton)==null||n.setAttr("aria-pressed",String(this.showInfo)),(a=this.labelButton)==null||a.toggleClass("is-active",this.plugin.settings.showLobeLabels),(c=this.labelButton)==null||c.setAttr("aria-pressed",String(this.plugin.settings.showLobeLabels));let o=k.filter(u=>e[u]).length;(l=this.allButton)==null||l.toggleClass("is-active",o===k.length),(s=this.noneButton)==null||s.toggleClass("is-active",o===0);for(let u of k){let f=this.lobeButtons[u];f&&(f.toggleClass("is-active",e[u]),f.setAttr("aria-pressed",String(e[u])))}}syncLegend(e){var i;if(!this.legendEl)return;this.legendEl.empty(),this.legendEl.toggleClass("is-hidden",!this.plugin.settings.showLegendChip),this.legendEl.createDiv({cls:"brain-atlas-legend-title",text:"Anatomical regions"});let o=this.renderer.getLobeStats();for(let n of Object.keys(M)){let a=M[n],c=Pr(n,e),l=this.plugin.settings.enabledLobes[n],s=this.legendEl.createDiv({cls:"brain-atlas-legend-row"});s.toggleClass("is-disabled",!l),s.setAttr("role","button"),s.setAttr("aria-pressed",String(l)),s.addEventListener("mouseenter",()=>this.renderer.setHighlightLobe(n)),s.addEventListener("mouseleave",()=>this.renderer.setHighlightLobe(null)),s.addEventListener("click",()=>this.toggleLobe(n)),s.createSpan({cls:"brain-atlas-swatch"}).style.setProperty("--brain-atlas-swatch",c);let u=s.createDiv({cls:"brain-atlas-legend-copy"});u.createSpan({cls:"brain-atlas-legend-label",text:a.label}),u.createSpan({cls:"brain-atlas-legend-sub",text:Ar(n)}),s.createSpan({cls:"brain-atlas-legend-count",text:String((i=o[n])!=null?i:0).padStart(2,"0")})}}syncTooltip(){if(!this.tooltipEl)return;let e=this.renderer.getHoveredNode();this.tooltipEl.toggleClass("is-visible",!!e),e&&(this.tooltipEl.empty(),this.tooltipEl.createDiv({cls:"brain-atlas-tooltip-title",text:be(e)}),this.tooltipEl.createDiv({cls:"brain-atlas-tooltip-sub",text:`${e.kindLabel} - ${e.degree} links`}),this.tooltipEl.createDiv({cls:"brain-atlas-tooltip-source",text:`classified by ${Qt(e.classificationSource)}`}),this.tooltipEl.createDiv({cls:"brain-atlas-tooltip-path",text:et(e)}))}syncFocusCard(){if(!this.focusEl)return;let e=this.renderer.getFocusedNode();this.focusEl.toggleClass("is-visible",!!e),e&&(this.focusEl.empty(),this.focusEl.createDiv({cls:"brain-atlas-focus-meta",text:`${e.kindLabel} - ${Qt(e.classificationSource)} - ${e.status.toUpperCase()}`}),this.focusEl.createDiv({cls:"brain-atlas-focus-title",text:be(e)}),this.focusEl.createDiv({cls:"brain-atlas-focus-sub",text:`${e.degree} links - ${et(e)}`}),this.isCoarsePointer()&&this.focusEl.createDiv({cls:"brain-atlas-focus-hint",text:"Tap again to open"}))}syncInfoPanel(){if(this.infoEl){if(this.infoEl.toggleClass("is-visible",this.showInfo),!this.showInfo){this.infoEl.empty();return}this.infoEl.empty(),this.infoEl.createDiv({cls:"brain-atlas-info-title",text:"What am I seeing?"}),this.infoEl.createDiv({cls:"brain-atlas-info-copy",text:"Dots are Markdown notes. Lines are wikilinks and embeds resolved from Obsidian metadata."}),this.infoEl.createDiv({cls:"brain-atlas-info-copy",text:"Regions come from frontmatter, tags, folders, daily-note names, then your default category and optional link behavior."}),this.infoEl.createDiv({cls:"brain-atlas-info-copy",text:"Region buttons isolate lobes. Labels toggles note and region text."})}}shouldPreviewBeforeOpen(e){if(!this.isCoarsePointer())return!1;let o=performance.now(),i=this.pendingOpenNodeId===e.id&&o-this.pendingOpenAt<1800;return this.pendingOpenNodeId=e.id,this.pendingOpenAt=o,this.syncFocusCard(),!i}isCoarsePointer(){var e,o;return(o=(e=window.matchMedia)==null?void 0:e.call(window,"(pointer: coarse)").matches)!=null?o:!1}openNode(e){let o=this.plugin.app.vault.getAbstractFileByPath(e.id);o instanceof fe.TFile&&this.plugin.app.workspace.getLeaf(this.plugin.settings.clickAction==="new-pane").openFile(o)}pinNode(e,o){this.plugin.settings={...this.plugin.settings,pinnedNodePositions:{...this.plugin.settings.pinnedNodePositions,[e.id]:o}},this.plugin.saveSettings()}toggleLabels(){this.plugin.settings.showLobeLabels=!this.plugin.settings.showLobeLabels,this.renderer.setOptions({showLobeLabels:this.plugin.settings.showLobeLabels}),this.syncOverlays(),this.persistViewSettings()}toggleInfo(){this.showInfo=!this.showInfo,this.syncOverlays()}toggleLobe(e){let o=this.plugin.settings.enabledLobes[e];this.plugin.settings.enabledLobes=Ce(this.plugin.settings.enabledLobes,e,!o),this.renderer.setOptions({enabledLobes:this.plugin.settings.enabledLobes}),this.syncOverlays(),this.persistViewSettings()}setAllRegions(e){this.plugin.settings.enabledLobes=st(e),this.renderer.setOptions({enabledLobes:this.plugin.settings.enabledLobes}),this.syncOverlays(),this.persistViewSettings()}async persistViewSettings(){await this.plugin.saveSettings(),this.plugin.refreshActiveBrainViews()}};function Jt(t){return{nodes:[],edges:[],idx:{},adj:{},KIND_LABEL:{},activePalette:{label:t.palette,bg:"#16151a",bgFar:"#0c0b0e",fg:"#e8e6e0",hud:"#c9b896",chroma:.4,kinds:{}},activePaletteName:t.palette,CHAOS:{wobbleAmp:0,wobbleSpeed:0,halo:.6,bloom:.5,blob:0,jitter:1}}}function Pr(t,r){var o;let e={frontal:"project",parietal:"concept",temporal:"person",occipital:"source",cerebellum:"dailyNote",stem:"index"}[t];return(o=r.activePalette.kinds[e])!=null?o:r.activePalette.hud}function Ar(t){switch(t){case"frontal":return"Projects - Decisions";case"parietal":return"Concepts - Tools";case"temporal":return"People - Orgs";case"occipital":return"Sources - Repos";case"cerebellum":return"Daily - Incidents";case"stem":return"Index - Routing"}}function Rr(t){switch(t){case"frontal":return"FRO";case"parietal":return"PAR";case"temporal":return"TEM";case"occipital":return"OCC";case"cerebellum":return"CER";case"stem":return"STM"}}function Qt(t){switch(t){case"frontmatter":return"frontmatter";case"tag":return"tag";case"folder":return"folder";case"filename":return"filename";case"linkBehavior":return"link behavior";case"default":return"default category"}}var Fe=class extends Te.Plugin{constructor(){super(...arguments);this.settings=We(null);this.debouncedRefresh=Er(()=>{try{this.refreshActiveBrainViews()}catch(e){console.error("Brain Atlas refresh failed",e),new Te.Notice("Brain Atlas refresh failed. See console for details.")}},750)}async onload(){let e=await this.loadData();this.settings=We(e),this.registerView(xe,o=>new ve(o,this)),this.addCommand({id:"open-view",name:"Open atlas",callback:()=>this.activateView()}),this.addRibbonIcon("brain","Open atlas",()=>this.activateView()),this.addSettingTab(new Ne(this)),this.registerEvent(this.app.metadataCache.on("resolved",()=>this.debouncedRefresh())),this.registerEvent(this.app.metadataCache.on("changed",()=>this.debouncedRefresh())),this.registerEvent(this.app.vault.on("create",()=>this.debouncedRefresh())),this.registerEvent(this.app.vault.on("delete",()=>this.debouncedRefresh())),this.registerEvent(this.app.vault.on("rename",()=>this.debouncedRefresh()))}async saveSettings(){await this.saveData(this.settings)}async activateView(){await this.app.workspace.getLeaf(!0).setViewState({type:xe,active:!0})}refreshActiveBrainViews(){for(let e of this.app.workspace.getLeavesOfType(xe)){let o=e.view;o instanceof ve&&o.rebuild()}}};function Er(t,r){let e=null;return()=>{e!==null&&window.clearTimeout(e),e=window.setTimeout(t,r)}}

/* nosourcemap */