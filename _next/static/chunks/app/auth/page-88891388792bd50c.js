(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[235],{785:function(e,r,t){Promise.resolve().then(t.bind(t,2476))},7907:function(e,r,t){"use strict";var n=t(5313);t.o(n,"useRouter")&&t.d(r,{useRouter:function(){return n.useRouter}})},2476:function(e,r,t){"use strict";t.r(r),t.d(r,{default:function(){return m}});var n=t(7437),o=t(575),i=t(5671),s=t(2782),a=t(248),l=t(2670),d=t(1270),u=t(9497),c=t(7907);let f=a.ZP.object({email:a.ZP.string().email()});function m(){let e=(0,c.useRouter)(),r=(0,l.cI)({resolver:(0,d.F)(f),defaultValues:{email:""}});async function t(r){console.log(r),e.push("/auth/otp")}return(0,n.jsxs)(i.Zb,{className:"mx-auto max-w-sm",children:[(0,n.jsxs)(i.Ol,{children:[(0,n.jsx)(i.ll,{className:"text-2xl",children:"Login"}),(0,n.jsx)(i.SZ,{children:"Enter your email below to login to your account"})]}),(0,n.jsx)(i.aY,{children:(0,n.jsx)(u.l0,{...r,children:(0,n.jsx)("form",{onSubmit:r.handleSubmit(t),className:"space-y-8",children:(0,n.jsxs)("div",{className:"grid gap-4",children:[(0,n.jsx)(u.Wi,{control:r.control,name:"email",rules:{required:"Pflichtfeld"},render:e=>{let{field:r}=e;return(0,n.jsxs)(u.xJ,{className:"grid gap-4",children:[(0,n.jsx)(u.lX,{children:"Email"}),(0,n.jsx)(u.NI,{children:(0,n.jsx)(s.I,{placeholder:"name.nachname",...r})}),(0,n.jsx)(u.zG,{})]})}}),(0,n.jsx)(o.z,{type:"submit",className:"w-full",children:"Login"})]})})})})]})}},575:function(e,r,t){"use strict";t.d(r,{d:function(){return l},z:function(){return d}});var n=t(7437),o=t(2265),i=t(9143),s=t(7742),a=t(2169);let l=(0,s.j)("inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",{variants:{variant:{default:"bg-primary text-primary-foreground hover:bg-primary/90",destructive:"bg-destructive text-destructive-foreground hover:bg-destructive/90",outline:"border border-input bg-background hover:bg-accent hover:text-accent-foreground",secondary:"bg-secondary text-secondary-foreground hover:bg-secondary/80",ghost:"hover:bg-accent hover:text-accent-foreground",link:"text-primary underline-offset-4 hover:underline"},size:{default:"h-10 px-4 py-2",sm:"h-9 rounded-md px-3",lg:"h-11 rounded-md px-8",icon:"h-10 w-10"}},defaultVariants:{variant:"default",size:"default"}}),d=o.forwardRef((e,r)=>{let{className:t,variant:o,size:s,asChild:d=!1,...u}=e,c=d?i.g7:"button";return(0,n.jsx)(c,{className:(0,a.cn)(l({variant:o,size:s,className:t})),ref:r,...u})});d.displayName="Button"},5671:function(e,r,t){"use strict";t.d(r,{Ol:function(){return a},SZ:function(){return d},Zb:function(){return s},aY:function(){return u},ll:function(){return l}});var n=t(7437),o=t(2265),i=t(2169);let s=o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)("div",{ref:r,className:(0,i.cn)("rounded-lg border bg-card text-card-foreground shadow-sm",t),...o})});s.displayName="Card";let a=o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)("div",{ref:r,className:(0,i.cn)("flex flex-col space-y-1.5 p-6",t),...o})});a.displayName="CardHeader";let l=o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)("h3",{ref:r,className:(0,i.cn)("text-2xl font-semibold leading-none tracking-tight",t),...o})});l.displayName="CardTitle";let d=o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)("p",{ref:r,className:(0,i.cn)("text-sm text-muted-foreground",t),...o})});d.displayName="CardDescription";let u=o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)("div",{ref:r,className:(0,i.cn)("p-6 pt-0",t),...o})});u.displayName="CardContent",o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)("div",{ref:r,className:(0,i.cn)("flex items-center p-6 pt-0",t),...o})}).displayName="CardFooter"},9497:function(e,r,t){"use strict";t.d(r,{l0:function(){return c},NI:function(){return h},pf:function(){return v},Wi:function(){return m},xJ:function(){return g},lX:function(){return b},zG:function(){return y}});var n=t(7437),o=t(2265),i=t(9143),s=t(2670),a=t(2169),l=t(4602);let d=(0,t(7742).j)("text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"),u=o.forwardRef((e,r)=>{let{className:t,...o}=e;return(0,n.jsx)(l.f,{ref:r,className:(0,a.cn)(d(),t),...o})});u.displayName=l.f.displayName;let c=s.RV,f=o.createContext({}),m=e=>{let{...r}=e;return(0,n.jsx)(f.Provider,{value:{name:r.name},children:(0,n.jsx)(s.Qr,{...r})})},x=()=>{let e=o.useContext(f),r=o.useContext(p),{getFieldState:t,formState:n}=(0,s.Gc)(),i=t(e.name,n);if(!e)throw Error("useFormField should be used within <FormField>");let{id:a}=r;return{id:a,name:e.name,formItemId:"".concat(a,"-form-item"),formDescriptionId:"".concat(a,"-form-item-description"),formMessageId:"".concat(a,"-form-item-message"),...i}},p=o.createContext({}),g=o.forwardRef((e,r)=>{let{className:t,...i}=e,s=o.useId();return(0,n.jsx)(p.Provider,{value:{id:s},children:(0,n.jsx)("div",{ref:r,className:(0,a.cn)("space-y-2",t),...i})})});g.displayName="FormItem";let b=o.forwardRef((e,r)=>{let{className:t,...o}=e,{error:i,formItemId:s}=x();return(0,n.jsx)(u,{ref:r,className:(0,a.cn)(i&&"text-destructive",t),htmlFor:s,...o})});b.displayName="FormLabel";let h=o.forwardRef((e,r)=>{let{...t}=e,{error:o,formItemId:s,formDescriptionId:a,formMessageId:l}=x();return(0,n.jsx)(i.g7,{ref:r,id:s,"aria-describedby":o?"".concat(a," ").concat(l):"".concat(a),"aria-invalid":!!o,...t})});h.displayName="FormControl";let v=o.forwardRef((e,r)=>{let{className:t,...o}=e,{formDescriptionId:i}=x();return(0,n.jsx)("p",{ref:r,id:i,className:(0,a.cn)("text-sm text-muted-foreground",t),...o})});v.displayName="FormDescription";let y=o.forwardRef((e,r)=>{let{className:t,children:o,...i}=e,{error:s,formMessageId:l}=x(),d=s?String(null==s?void 0:s.message):o;return d?(0,n.jsx)("p",{ref:r,id:l,className:(0,a.cn)("text-sm font-medium text-destructive",t),...i,children:d}):null});y.displayName="FormMessage"},2782:function(e,r,t){"use strict";t.d(r,{I:function(){return s}});var n=t(7437),o=t(2265),i=t(2169);let s=o.forwardRef((e,r)=>{let{className:t,type:o,...s}=e;return(0,n.jsx)("input",{type:o,className:(0,i.cn)("flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",t),ref:r,...s})});s.displayName="Input"},2169:function(e,r,t){"use strict";t.d(r,{cn:function(){return i}});var n=t(3167),o=t(1367);function i(){for(var e=arguments.length,r=Array(e),t=0;t<e;t++)r[t]=arguments[t];return(0,o.m6)((0,n.W)(r))}}},function(e){e.O(0,[363,594,971,69,744],function(){return e(e.s=785)}),_N_E=e.O()}]);