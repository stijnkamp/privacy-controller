(window.webpackJsonp=window.webpackJsonp||[]).push([[10],{584:function(e,t,r){"use strict";r.r(t);r(33),r(24),r(23),r(10),r(36),r(28),r(37);var l=r(16),n=r(38);function c(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,r)}return t}var o={name:"DeviceList",data:function(){return{interval:null}},computed:function(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?c(Object(source),!0).forEach((function(t){Object(l.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):c(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}({},Object(n.d)({devices:function(e){return e.devices.devices}})),methods:{showDevice:function(e){this.$router.push("/devices/"+e.id)},blockDevice:function(e){this.$store.dispatch("devices/blockDevice",e.pihole_device_id)}}},v=o,d=r(15),f=Object(d.a)(v,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return e.devices.length?r("div",{staticClass:"bg-white shadow overflow-hidden sm:rounded-md"},[e._m(0),e._v(" "),r("ul",{staticClass:"divide-y divide-gray-200 overflow-auto new-device-list",attrs:{role:"list"}},e._l(e.devices,(function(t){return r("li",{key:t.id,staticClass:"block hover:bg-gray-50"},[r("div",{staticClass:"px-4 py-4 flex items-center sm:px-6"},[r("div",{staticClass:"min-w-0 flex-1 sm:flex sm:items-center sm:justify-between"},[r("div",{staticClass:"truncate"},[r("div",{staticClass:"flex text-sm"},[r("p",{staticClass:"font-medium text-blue-600 truncate"},[e._v(e._s(t.name?t.name:"Unknown name"))]),e._v(" "),r("p",{staticClass:"ml-1 flex-shrink-0 font-normal text-gray-500"},[e._v(e._s(t.pihole_device.macVendor?t.macVendor:""))])]),e._v(" "),r("div",{staticClass:"mt-2 flex"},[r("div",{staticClass:"flex items-center text-sm text-gray-500"},[r("i",{staticClass:"la la-lg la-clock mr-2"}),e._v(" "),r("p",[e._v("\n                                    First seen "+e._s(e._f("formatDate")(t.pihole_device.firstSeen,"LLL"))),r("br"),e._v("\n                                    Last active "+e._s(e._f("formatDate")(t.pihole_device.lastQuery,"fromNow"))+" ago\n                                ")])])])])]),e._v(" "),r("div",{staticClass:"ml-5 flex-shrink-0 flex flex-col"},[r("div",{staticClass:"flex justify-between items-center px-4 py-2 rounded-full text-xs font-medium bg-green-100 text-green-800 cursor-pointer",on:{click:function(r){return e.showDevice(t)}}},[r("i",{staticClass:"la la-lg la-eye mr-2"}),e._v("\n                        Show\n                    ")]),e._v(" "),r("div",{staticClass:"inline-flex items-center px-4 py-2 rounded-full text-xs font-medium bg-red-100 text-red-800 mt-2 cursor-pointer",on:{click:function(t){return e.blockDevice()}}},[r("i",{staticClass:"la la-lg la-ban mr-2"}),e._v("\n                        Block\n                    ")])])])])})),0)]):e._e()}),[function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"bg-white px-4 py-5 border-b border-gray-200 sm:px-6 items-center flex"},[r("i",{staticClass:"la la-2x la-laptop text-blue-400"}),e._v(" "),r("h3",{staticClass:"text-lg leading-6 font-medium text-gray-900 ml-2"},[e._v("Devices")])])}],!1,null,null,null).exports,m=r(520),_=r(504),h=r.n(_),y=(r(39),r(522)),x=r(508),C=r(152);function w(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,r)}return t}function O(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?w(Object(source),!0).forEach((function(t){Object(l.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):w(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var j={name:"TrafficFilter",components:{Card:y.a,Dropdown:x.a},data:function(){return{filter:{devices:[],server_groups:[],locations:[],companies:[],group_by:"src"}}},mounted:function(){this.getDevices(),this.getFilters()},watch:{filter:{handler:function(){this.applyFilter()},deep:!0}},computed:O(O({},Object(n.d)({devices:function(e){return e.devices.devices},serverGroups:function(e){return e.traffic.filterOptions.serverGroups},locations:function(e){return e.traffic.filterOptions.locations},companies:function(e){return e.traffic.filterOptions.companies}})),{},{allDevices:{get:function(){return this.filter.devices.length===this.devices.length?[!0]:[]},set:function(e){return this.filter.devices=e.length>0?this.devices.map((function(e){return e.id})):[]}},allServerGroups:{get:function(){return this.filter.server_groups.length===this.serverGroups.length?[!0]:[]},set:function(e){return this.filter.server_groups=e.length>0?this.serverGroups.map((function(e){return e.id})):[]}},allLocations:{get:function(){return this.filter.locations.length===this.locations.length?[!0]:[]},set:function(e){return this.filter.locations=e.length>0?this.locations.map((function(e){return e.id})):[]}},allCompanies:{get:function(){return this.filter.companies.length===this.companies.length?[!0]:[]},set:function(e){return this.filter.companies=e.length>0?this.companies.map((function(e){return e.id})):[]}},groupToggle:{get:function(){return"dst"===this.filter.group_by?"Receiving":"Sending"},set:function(e){this.filter.group_by="Receiving"===e?"dst":"src"}}}),methods:O(O(O({},Object(n.b)("devices",["getDevices"])),Object(n.b)("traffic",["getFilters"])),{},{applyFilter:function(){this.$emit("update:filter",Object(C.cloneDeep)(this.filter))}})},k={components:{TrafficFilter:Object(d.a)(j,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("card",{attrs:{icon:{color:"blue",name:"filter"},title:"Filter"}},[r("div",{staticClass:"px-4 divide-y divide-gray-200"},[r("div",[r("label",{staticClass:"block"},[r("input",{directives:[{name:"model",rawName:"v-model",value:e.filter.group_by,expression:"filter.group_by"}],attrs:{type:"radio",name:"group",value:"src"},domProps:{checked:e._q(e.filter.group_by,"src")},on:{change:function(t){return e.$set(e.filter,"group_by","src")}}}),e._v(" Show from which local devices data is send")]),e._v(" "),r("label",{staticClass:"block"},[r("input",{directives:[{name:"model",rawName:"v-model",value:e.filter.group_by,expression:"filter.group_by"}],attrs:{type:"radio",name:"group",value:"dst"},domProps:{checked:e._q(e.filter.group_by,"dst")},on:{change:function(t){return e.$set(e.filter,"group_by","dst")}}}),e._v(" Show to which servers data is send")])]),e._v(" "),r("dropdown",{attrs:{"start-open":!0},scopedSlots:e._u([{key:"trigger",fn:function(){return[r("div",{staticClass:"py-2"},[e._v("\n                        Devices\n                    ")])]},proxy:!0}])},[e._v(" "),r("div",[r("div",{staticClass:"divide-y divide-gray-200"},[r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center"},[r(h.a,{attrs:{id:"device-all",value:!0},model:{value:e.allDevices,callback:function(t){e.allDevices=t},expression:"allDevices"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"device-all"}},[r("div",{staticClass:"font-medium"},[e._v("All devices")])])]),e._v(" "),e._l(e.devices,(function(t){return r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center h-5"},[r(h.a,{attrs:{size:"sm",id:"device-"+t.id,name:"city",value:t.id},model:{value:e.filter.devices,callback:function(t){e.$set(e.filter,"devices",t)},expression:"filter.devices"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"device-"+t.id}},[r("div",[e._v(e._s(t.name))])])])}))],2)])]),e._v(" "),r("dropdown",{scopedSlots:e._u([{key:"trigger",fn:function(){return[r("div",{staticClass:"py-2"},[e._v("\n                        Server groups\n                    ")])]},proxy:!0}])},[e._v(" "),r("div",[r("div",{staticClass:"divide-y divide-gray-200"},[r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center"},[r(h.a,{attrs:{id:"server-group-all",value:!0},model:{value:e.allServerGroups,callback:function(t){e.allServerGroups=t},expression:"allServerGroups"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"server-group-all"}},[r("div",{staticClass:"font-medium"},[e._v("All server groups")])])]),e._v(" "),e._l(e.serverGroups,(function(t){return r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center h-5"},[r(h.a,{attrs:{size:"sm",id:"server-group-"+t.id,name:"city",value:t.id},model:{value:e.filter.server_groups,callback:function(t){e.$set(e.filter,"server_groups",t)},expression:"filter.server_groups"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"server-group-"+t.id}},[r("div",[e._v(e._s(t.name))])])])}))],2)])]),e._v(" "),r("dropdown",{scopedSlots:e._u([{key:"trigger",fn:function(){return[r("div",{staticClass:"py-2"},[e._v("\n                        Locations\n                    ")])]},proxy:!0}])},[e._v(" "),r("div",[r("div",{staticClass:"divide-y divide-gray-200"},[r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center"},[r(h.a,{attrs:{id:"location-all",value:!0},model:{value:e.allLocations,callback:function(t){e.allLocations=t},expression:"allLocations"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"location-all"}},[r("div",{staticClass:"font-medium"},[e._v("All locations")])])]),e._v(" "),e._l(e.locations,(function(t){return r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center h-5"},[r(h.a,{attrs:{size:"sm",id:"location-"+t,name:"city",value:t},model:{value:e.filter.locations,callback:function(t){e.$set(e.filter,"locations",t)},expression:"filter.locations"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"location-"+t}},[r("div",[e._v(e._s(t))])])])}))],2)])]),e._v(" "),r("dropdown",{scopedSlots:e._u([{key:"trigger",fn:function(){return[r("div",{staticClass:"py-2"},[e._v("\n                        Companies\n                    ")])]},proxy:!0}])},[e._v(" "),r("div",[r("div",{staticClass:"divide-y divide-gray-200"},[r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center"},[r(h.a,{attrs:{id:"company-all",value:!0},model:{value:e.allCompanies,callback:function(t){e.allCompanies=t},expression:"allCompanies"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"company-all"}},[r("div",{staticClass:"font-medium"},[e._v("All companies")])])]),e._v(" "),e._l(e.companies,(function(t){return r("div",{staticClass:"relative flex items-center py-2"},[r("div",{staticClass:"flex items-center h-5"},[r(h.a,{attrs:{size:"sm",id:"company-"+t.id,name:"city",value:t.id},model:{value:e.filter.companies,callback:function(t){e.$set(e.filter,"companies",t)},expression:"filter.companies"}})],1),e._v(" "),r("label",{staticClass:"min-w-0 flex-1 text-sm ml-3",attrs:{for:"company-"+t.id}},[r("div",[e._v(e._s(t.name))])])])}))],2)])])],1)])}),[],!1,null,"0d4a9c88",null).exports,TrafficChart:m.a,DeviceList:f},data:function(){return{text:null,filter:{}}}},D=Object(d.a)(k,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"p-6 flex flex-col"},[r("div",{staticClass:"grid grid-cols-4 flex-1 min-h-0 align-stretch"},[r("traffic-chart",{staticClass:"col-span-3",attrs:{filter:e.filter}}),e._v(" "),r("traffic-filter",{staticClass:"max-h-full overflow-auto",on:{"update:filter":function(t){e.filter=t}}})],1)])}),[],!1,null,null,null);t.default=D.exports}}]);