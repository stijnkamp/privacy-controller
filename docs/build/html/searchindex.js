Search.setIndex({docnames:["index","installation/hardware","installation/software","services/firewall","services/resolver","services/tracker","services/web","services/websocket","shared/config","shared/state","shared/thread","shared/utils","start_scripts/benchmark","start_scripts/main"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":3,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,sphinx:56},filenames:["index.rst","installation/hardware.rst","installation/software.rst","services/firewall.rst","services/resolver.rst","services/tracker.rst","services/web.rst","services/websocket.rst","shared/config.rst","shared/state.rst","shared/thread.rst","shared/utils.rst","start_scripts/benchmark.rst","start_scripts/main.rst"],objects:{"":{benchmark:[12,0,0,"-"],config:[8,0,0,"-"],firewall:[3,0,0,"-"],main:[13,0,0,"-"],resolver:[4,0,0,"-"],state:[9,0,0,"-"],thread:[10,0,0,"-"],tracker:[5,0,0,"-"],utils:[11,0,0,"-"],web:[6,0,0,"-"],websocket:[7,0,0,"-"]},"firewall.firewall_commands":{FirewallCommands:[3,2,1,""]},"firewall.firewall_commands.FirewallCommands":{get:[3,3,1,""],get_firewall_rules:[3,3,1,""],set_standard_rules:[3,3,1,""]},"firewall.rule_parser":{RuleParser:[3,2,1,""]},"firewall.rule_parser.RuleParser":{get_rules_for_devices:[3,3,1,""],get_service_settings:[3,3,1,""]},"resolver.Resolver":{get_dhcp_leases:[4,3,1,""]},"resolver.dns_lookup":{get_company_for_domain:[4,1,1,""],get_domain_for_ip:[4,1,1,""],get_location_for_ip:[4,1,1,""],reverse_dns:[4,1,1,""]},"resolver.helpers":{get_database_file:[4,1,1,""],get_dhcp_leases:[4,1,1,""],get_own_hwaddr:[4,1,1,""],get_pihole_config:[4,1,1,""]},"resolver.resolver_commands":{ResolverCommands:[4,2,1,""]},"resolver.resolver_commands.ResolverCommands":{get:[4,3,1,""],resolve_destinations:[4,3,1,""]},"state.State":{get_queue:[9,3,1,""],send_command:[9,3,1,""]},"thread.Thread":{running:[10,3,1,""],set_queue:[10,3,1,""],start:[10,3,1,""],stop:[10,3,1,""]},"tracker.Tracker":{getPacketKey:[5,3,1,""],packet_handler:[5,3,1,""]},"tracker.scapy_tracker":{ScapyTracker:[5,2,1,""]},"tracker.scapy_tracker.ScapyTracker":{get_packet_size:[5,3,1,""],parse_packet:[5,3,1,""],start:[5,3,1,""]},"tracker.tcp_dump_tracker":{TcpDumpTracker:[5,2,1,""],re_param:[5,1,1,""]},"tracker.tcp_dump_tracker.TcpDumpTracker":{parse_packet:[5,3,1,""],start:[5,3,1,""]},"web.controller":{Controller:[6,2,1,""]},"web.helpers":{add_relationship:[6,1,1,""],get_input:[6,1,1,""],get_or_create:[6,1,1,""],parse_model:[6,1,1,""]},"web.web_server":{WebServer:[6,2,1,""],catch_all:[6,1,1,""],docs:[6,1,1,""],docs_redirect:[6,1,1,""]},"web.web_server.WebServer":{setup_modules:[6,3,1,""]},"websocket.Websocket":{check_for_stop:[7,3,1,""],handler:[7,3,1,""],notify_clients:[7,3,1,""]},benchmark:{clear_buffer:[12,1,1,""],handle_packet:[12,1,1,""],receive_packet:[12,1,1,""],start:[12,1,1,""]},config:{get_service:[8,1,1,""],get_services:[8,1,1,""]},firewall:{Firewall:[3,2,1,""],firewall_commands:[3,0,0,"-"],rule_parser:[3,0,0,"-"]},main:{start:[13,1,1,""]},resolver:{Resolver:[4,2,1,""],dns_lookup:[4,0,0,"-"],helpers:[4,0,0,"-"],resolver_commands:[4,0,0,"-"]},state:{State:[9,2,1,""]},thread:{Thread:[10,2,1,""]},tracker:{Tracker:[5,2,1,""],scapy_tracker:[5,0,0,"-"],tcp_dump_tracker:[5,0,0,"-"]},utils:{get_current_thread_name:[11,1,1,""],get_json:[11,1,1,""],get_path:[11,1,1,""],is_ip4:[11,1,1,""],is_json:[11,1,1,""],log:[11,1,1,""],safe_run:[11,1,1,""],search_in_file:[11,1,1,""]},web:{controller:[6,0,0,"-"],helpers:[6,0,0,"-"],web_server:[6,0,0,"-"]},websocket:{Websocket:[7,2,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method"},terms:{"0x741d8790":[],"0x741d8970":[],"0x742108e0":[],"0x74210ac0":[],"0x7423b3d0":[],"0x7423b5b0":[],"0x7429b880":[],"0x7429ba60":[],"0x742e37a8":[],"0x742e3958":[],"0x7433f940":[],"0x7435f0a0":[],"0x743672c8":[],"0x743a7808":[],"0x743af118":[],"0x743c70b8":[],"0x743cead8":[],"0x743f4970":[],"0x74402748":[],"0x759b3130":[],"0x759b3148":[],"0x759b31a8":[],"0x759b3388":[],"0x75a05250":[],"0x75a05430":[],"0x75a1b1f0":[],"0x75a1b3d0":[],"168":[0,5],"16gb":1,"192":[0,5],"8888":0,"case":9,"class":[0,4,5,6,7,9],"default":[],"float":[],"function":[0,9,11],"int":[],"long":8,"new":[0,3,8,9],"return":[10,11],"static":6,"true":[],"try":0,And:9,But:2,DNS:2,For:8,One:0,That:8,The:[0,1,2,6,7,8,9,10,12,13],There:9,Using:0,_saferunerror:11,abl:0,access:[0,1,13],accord:[0,1,7],act:[0,1],activ:7,actual:10,add:[0,9],add_relationship:6,address:[0,8,11],after:2,again:3,all:[0,1,3,8,9,10,11,12,13],allianc:8,alliance_slug:8,allow:0,alreadi:3,also:[0,13],alwai:1,amount:0,ani:[0,9],anoth:9,api:6,app:8,appli:3,applic:[0,8],approach:3,arg:11,around:12,arrai:8,asset:8,async:[5,7],automat:9,awesom:8,base:[3,4,5,6,7,9,10],bash:2,been:9,belong:8,benchmark:0,between:[0,9],bigger:12,blacklist:3,block:0,bool:10,boot:2,build:8,cabl:1,can:[0,1,2,3,7,8,9,11,13],captur:12,card:[1,2],catch_al:6,certain:13,chang:8,channel:7,check:[3,10,12],check_for_stop:7,chmod:2,citi:[],classful:6,clear_buff:12,cli:2,client:7,clone:2,close:[10,13],cloud:[],cmd:[3,4,9,13],code:2,column:6,columndefault:[],com:2,command:[0,2,9,13],common:11,compani:[0,8],company_id:[],config:8,configur:[0,3],connect:[0,1,2,7],consist:11,contain:[3,11],content:0,contin:[],control:[1,2,8,12,13],could:8,countri:[],creat:3,credenti:1,current:[9,12],current_timestamp:[],data:[0,8],data_typ:8,data_type_id:[],databas:3,datatyp:8,date_cr:[],date_modifi:[],datetim:[],decl_api:[],dedic:8,depend:12,describ:8,descript:[0,8],destin:[0,4],devic:[0,1,3,8],device_data:8,device_id:[],device_statu:8,device_typ:8,device_type_id:[],devicefunction:8,devicetyp:8,dhcp:[2,9],dict:11,differ:[1,6,9],disabl:8,discov:0,dispatch:7,dns_lookup:0,doc:6,docs_redirect:6,doe:0,doing:8,domain:[4,8],done:[0,2,3,9],drop:[3,12],dst:[],each:[0,8],easi:1,enabl:[0,8],end:7,enhanc:0,enter:2,entir:[0,2],ethernet:1,everi:[8,11,12],everyth:0,exampl:8,execut:9,exit:13,express:8,extra:8,failur:11,fals:[],field:8,file:[6,8,11],filenam:11,filter:5,find_server_group_id:[],firewal:[0,13],firewall_command:3,firewallcommand:3,first:2,flask:[6,8],flask_class:6,flaskview:6,flow:0,folder:[8,13],follow:[0,2,8,13],format:2,from:[0,3,7,8,9,11],front:7,frontend:6,func:11,functionality_id:[],functionalityservic:[],furthermor:1,gatewai:[0,1,12],gener:[0,8,10,11],get:[3,4,7,11],get_company_for_domain:4,get_current_thread_nam:11,get_database_fil:4,get_dhcp_leas:4,get_domain_for_ip:4,get_firewall_rul:3,get_input:6,get_json:11,get_location_for_ip:4,get_or_cr:6,get_own_hwaddr:4,get_packet_s:5,get_path:11,get_pihole_config:4,get_queu:9,get_rules_for_devic:3,get_servic:8,get_service_set:3,getpacketkei:5,git:2,github:2,given:9,group:[0,8],guess:0,handl:[2,7,8],handle_packet:12,handler:[7,8],hardwar:[0,2],has:[0,3,8,9],have:[0,1,2,13],helper:0,here:0,home:[0,1,2,3],how:8,http:[0,2],hub:1,hwaddr:[],icon:8,identifi:8,imag:[2,8],implement:8,incom:8,inform:8,initi:[10,13],insert:2,insid:[0,2,3,8,13],instal:[0,3,8,13],instead:1,instruct:2,integ:[],intercept:3,investig:0,is_ip4:11,is_json:11,item:6,itself:[1,8],json:11,json_str:11,just:7,keep:7,kernel:3,known:[3,8],kwarg:[6,11],lat:[],latest:[],leas:9,length:12,light:8,like:[11,13],line:[5,8],link:[0,8],linux:[2,3],list:[],lite:2,load:12,local:[0,2,3,8],locat:0,location_id:[],lock:10,log:[10,11],login:[1,2],logo:[],lon:[],machin:0,main:[0,2,9],mainli:12,make:[1,8,13],manag:13,materi:1,messag:[7,9],minimum:1,mode:1,model:6,modul:0,monitor:13,most:[2,3],multipl:[8,13],name:[3,5,8,10],need:[1,2,3,8,9,13],net:5,network:[0,1,8],next:3,none:6,notify_cli:7,npm:[],nullabl:[],number:12,obj:11,object:[3,4,5,9,10],offer:8,one:8,onlin:8,onupd:[],option:8,order:[1,3,8],organ:8,orm:[],other:[0,6,8,10],otherwis:1,outgo:0,outsid:0,own:[0,1],packag:[3,8],packet:[0,3,5,12],packet_handl:5,paramet:[6,7,10],parse_model:6,parse_packet:5,password:2,path:[6,7,8],pattern:5,permiss:13,pihol:2,pihole_devic:[],pihole_device_id:[],pkt:5,pm2:[2,13],point:1,port:5,possibl:8,previou:2,primary_kei:[],privaci:[0,2,13],privat:[0,2],privatehom:1,process:12,program:[3,13],project:13,properti:[],proto:[],provid:[6,8],purpos:2,put:3,python:13,queri:8,queu:10,queue:[3,7],raspberri:2,re_param:5,readabl:8,real:7,receive_packet:12,regex:[8,11],region:[],regist:[6,7],rel:[1,8],relationship:6,rememb:1,repres:8,requir:2,resolv:0,resolve_destin:4,resolver_command:0,resolvercommand:4,rest:[0,6],retriev:12,reverse_dn:4,root:13,router:[],rule:3,rule_pars:3,rulepars:0,run:[0,2,3,7,10],safe_run:11,sai:8,same:[2,3],save:13,scapy_track:0,scapytrack:5,scheme:1,script:2,search_in_fil:11,second:8,section:2,see:1,send:[0,7,8,9,12],send_cloud_command:8,send_command:9,separ:8,serv:6,server:[0,2,8],server_group:8,server_group_id:[],server_group_slug:8,server_id:[],servergroup:8,servergroupqueri:8,serverqueri:[],servic:[9,10,11,13],service_data:[],service_id:[],service_slug:8,servicedata:[],session:6,set:[3,8,13],set_queu:10,set_standard_rul:3,setup:[0,2,3,13],setup_modul:6,share:[6,9,10,13],should:[1,2,10],situat:12,size:0,slug:8,smart:[0,1,3],sock:12,softwar:0,some:[8,9,11],someth:9,sourc:2,specif:[0,7,8],sql:[],sqlalchemi:[],src:5,ssh:5,stack:11,standard:3,start:[5,7,10,12,13],startup:[2,13],state:[0,3,4,5,6,7,10,13],stijnkamp:2,still:10,stop:10,storag:[1,8],store:8,str:[7,8,10],structur:8,sub:10,submodul:0,subpackag:[],subscrib:7,sudo:[2,13],sup:13,sure:[1,13],system:[0,1,12],tabl:0,take:3,task:10,tcp:[0,12],tcp_dump:12,tcp_dump_track:0,tcpdumptrack:5,termin:10,test:2,thei:8,them:[2,3],thi:[0,3,8,9],thing:0,those:[3,7,13],thread:[3,4,5,6,7,13],through:[0,1,7,12],time:7,timestamp:[],total:12,trace:11,track:0,tracker:[0,12],traffic:0,trigger:8,tuya:8,tuya_serv:8,two:0,type:[8,10],unfortun:12,uniqu:8,until:7,updat:[3,7,9],upon:11,usb:1,use:[8,11,13],used:[0,3,12],user:8,using:[0,2,8],util:0,variabl:8,version:3,wait:[3,9],want:[0,3],watch:7,web:[0,8],web_serv:6,webserv:6,websocket:[0,8],websocketcli:7,what:8,when:[0,2,3,8,9,13],where:0,which:[0,3,7,8],who:[0,7],wifi:[1,2],work:[0,2],worker:9,world:0,you:[0,1,2,8,9,13],your:[0,1,3,8]},titles:["Welcome to PrivateHome\u2019s documentation!","<span class=\"section-number\">1. </span>Hardware installation","<span class=\"section-number\">2. </span>Software installation","<span class=\"section-number\">1. </span>Firewall Service","<span class=\"section-number\">2. </span>Resolver Service","<span class=\"section-number\">3. </span>Tracker Service","<span class=\"section-number\">4. </span>Web Service","<span class=\"section-number\">5. </span>Websocket Service","<span class=\"section-number\">1. </span>Configuration","<span class=\"section-number\">2. </span>State","Thread class","<span class=\"section-number\">3. </span>Utils helpers","<span class=\"section-number\">2. </span>benchmark.py script","<span class=\"section-number\">1. </span>main.py script"],titleterms:{"class":[3,10,13],"function":[3,8,13],access:2,api:[],applic:2,benchmark:12,boot:13,command:3,configur:8,content:[4,5,6,7],control:[0,6],dashboard:0,dns_lookup:4,document:0,firewal:3,flow:3,gener:3,hardwar:1,helper:[4,6,11],home:8,inform:0,instal:[1,2],json:8,main:13,model:[],modul:[4,5,6,7],monitor:0,oper:2,packag:2,privatehom:0,purpos:0,queue:9,raspberri:1,requir:1,resolv:4,resolver_command:4,router:1,rulepars:3,run:13,scapy_track:5,script:[0,12,13],servic:[0,3,4,5,6,7,8],setup:1,share:0,smart:8,softwar:2,ssh:2,start:[0,2],state:9,submodul:[4,5,6],subpackag:[],system:[2,9],tabl:3,tcp_dump_track:5,thread:10,tracker:5,util:11,variabl:0,web:6,websocket:7,welcom:0}})