Search.setIndex({docnames:["client","common","index","pyqt_ui","server"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["client.rst","common.rst","index.rst","pyqt_ui.rst","server.rst"],objects:{"":[[0,0,0,"-","client"],[1,0,0,"-","common"],[3,0,0,"-","pyqt_ui"],[4,0,0,"-","server"]],"client.client":[[0,1,1,"","Client"],[0,1,1,"","ReceiverThread"],[0,1,1,"","SendTask"],[0,1,1,"","SenderThread"],[0,4,1,"","create_socket"]],"client.client.Client":[[0,2,1,"","account_name"],[0,3,1,"","add_contact"],[0,3,1,"","del_contact"],[0,3,1,"","get_contact_list"],[0,3,1,"","login"],[0,3,1,"","logout"],[0,3,1,"","send"],[0,3,1,"","sign_up"],[0,3,1,"","stopped"],[0,3,1,"","subscribe_to_messages"]],"client.client.ReceiverThread":[[0,3,1,"","run"],[0,3,1,"","stop"],[0,2,1,"","stopped"],[0,3,1,"","subscribe_to_messages"]],"client.client.SenderThread":[[0,3,1,"","run"],[0,3,1,"","submit_task"]],"client.client_repository":[[0,1,1,"","ClientRepository"]],"client.client_repository.ClientRepository":[[0,1,1,"","Base"],[0,1,1,"","MessageHistory"],[0,1,1,"","MyContacts"],[0,3,1,"","add_contact"],[0,3,1,"","check_contact"],[0,3,1,"","del_contact"],[0,3,1,"","get_contact_list"],[0,3,1,"","get_message_history"],[0,3,1,"","save_message"]],"client.client_repository.ClientRepository.Base":[[0,5,1,"","metadata"],[0,5,1,"","registry"]],"client.client_repository.ClientRepository.MessageHistory":[[0,5,1,"","date"],[0,5,1,"","from_acc"],[0,5,1,"","id"],[0,5,1,"","message"],[0,5,1,"","to_acc"]],"client.client_repository.ClientRepository.MyContacts":[[0,5,1,"","login"],[0,5,1,"","name"]],"common.descriptor":[[1,1,1,"","Port"]],"common.messages":[[1,1,1,"","AuthenticateFieldName"],[1,1,1,"","ClientRequestFieldName"],[1,1,1,"","MessageType"],[1,1,1,"","MsgFieldName"],[1,1,1,"","RequestToServer"],[1,1,1,"","ResponseCode"],[1,1,1,"","ServerResponseFieldName"],[1,1,1,"","UserFieldName"]],"common.messages.AuthenticateFieldName":[[1,5,1,"","PASSWORD"]],"common.messages.ClientRequestFieldName":[[1,5,1,"","ACTION"]],"common.messages.MessageType":[[1,5,1,"","ADD_CONTACT"],[1,5,1,"","AUTHENTICATE"],[1,5,1,"","DEL_CONTACT"],[1,5,1,"","GET_CONTACTS"],[1,5,1,"","MESSAGE"],[1,5,1,"","PRESENCE"],[1,5,1,"","SIGN_UP"]],"common.messages.MsgFieldName":[[1,5,1,"","FROM"],[1,5,1,"","MESSAGE"],[1,5,1,"","TIME"],[1,5,1,"","TO"]],"common.messages.RequestToServer":[[1,5,1,"","USER_ID"],[1,5,1,"","USER_LOGIN"]],"common.messages.ResponseCode":[[1,5,1,"","ACCEPTED"],[1,5,1,"","BAD_REQUEST"],[1,5,1,"","CONFLICT"],[1,5,1,"","INTERNAL_SERVER_ERROR"],[1,5,1,"","OK"],[1,5,1,"","UNAUTHORIZED"]],"common.messages.ServerResponseFieldName":[[1,5,1,"","ALERT"],[1,5,1,"","ERROR"],[1,5,1,"","RESPONSE"],[1,5,1,"","TIME"]],"common.messages.UserFieldName":[[1,5,1,"","ACCOUNT"],[1,5,1,"","BIRTHDATE"],[1,5,1,"","LOGIN"],[1,5,1,"","NAME"],[1,5,1,"","SURNAME"],[1,5,1,"","USER"]],"common.utils":[[1,4,1,"","get_data"],[1,4,1,"","send_message"]],"common.verifiers":[[1,1,1,"","ClientVerifier"],[1,1,1,"","ServerVerifier"]],"pyqt_ui.admin_page":[[3,1,1,"","Admin"]],"pyqt_ui.admin_page.Admin":[[3,3,1,"","create_read_only_cell"],[3,3,1,"","del_user"],[3,3,1,"","load_server_settings"],[3,3,1,"","load_stats"],[3,3,1,"","load_users"],[3,3,1,"","save_server_settings"],[3,3,1,"","show_file_dialog"],[3,3,1,"","tab_changed"]],"pyqt_ui.main":[[3,1,1,"","AccountForm"],[3,1,1,"","LoginForm"],[3,1,1,"","SignUpForm"],[3,1,1,"","WelcomeForm"]],"pyqt_ui.main.AccountForm":[[3,5,1,"","add_contact_signal"],[3,3,1,"","add_contact_to_list"],[3,5,1,"","cont_list_signal"],[3,3,1,"","del_contact_from_list"],[3,5,1,"","del_contact_signal"],[3,3,1,"","handle_contacts_response"],[3,3,1,"","message_received"],[3,3,1,"","message_sent"],[3,5,1,"","message_sent_signal"],[3,5,1,"","receive_message_signal"],[3,3,1,"","remove_contact"],[3,3,1,"","send_btn_clicked"],[3,3,1,"","set_current_chat"],[3,3,1,"","show_new_contact"]],"pyqt_ui.main.LoginForm":[[3,3,1,"","back_to_welcome"],[3,3,1,"","connect_to_chat"],[3,5,1,"","login_signal"],[3,3,1,"","show_account_form"]],"pyqt_ui.main.SignUpForm":[[3,3,1,"","back_to_welcome"],[3,3,1,"","show_account_form"],[3,3,1,"","sign_up_for_messenger"],[3,5,1,"","sign_up_signal"]],"pyqt_ui.main.WelcomeForm":[[3,3,1,"","go_to_login"],[3,3,1,"","sign_up_for_messenger"]],"server.repository":[[4,1,1,"","Repository"],[4,4,1,"","set_sqlite_pragma"]],"server.repository.Repository":[[4,1,1,"","Base"],[4,1,1,"","Contact"],[4,1,1,"","User"],[4,1,1,"","UserHistory"],[4,3,1,"","add_contact"],[4,3,1,"","add_history"],[4,3,1,"","add_user"],[4,3,1,"","connect_to_messenger"],[4,3,1,"","del_contact"],[4,3,1,"","del_user"],[4,3,1,"","get_all_user_history"],[4,3,1,"","get_contacts"],[4,3,1,"","get_hash"],[4,3,1,"","get_user"],[4,3,1,"","get_user_history"],[4,3,1,"","load_users"],[4,3,1,"","sign_up"]],"server.repository.Repository.Base":[[4,5,1,"","metadata"],[4,5,1,"","registry"]],"server.repository.Repository.Contact":[[4,5,1,"","contact_id"],[4,5,1,"","contact_login"],[4,5,1,"","owner_login"]],"server.repository.Repository.User":[[4,5,1,"","birthdate"],[4,5,1,"","login"],[4,5,1,"","name"],[4,5,1,"","password_hash"],[4,5,1,"","salt"],[4,5,1,"","surname"]],"server.repository.Repository.UserHistory":[[4,5,1,"","client_id"],[4,5,1,"","ip_address"],[4,5,1,"","login"],[4,5,1,"","login_time"]],"server.server_utils":[[4,4,1,"","create_response"],[4,4,1,"","remove_from_list"],[4,4,1,"","remove_if_present"],[4,4,1,"","validate_add_contact"],[4,4,1,"","validate_authenticate"],[4,4,1,"","validate_del_contact"],[4,4,1,"","validate_get_contact"],[4,4,1,"","validate_presence"],[4,4,1,"","validate_sign_up"],[4,4,1,"","validate_user_msg"]],"server.utils":[[4,4,1,"","get_config"],[4,4,1,"","get_config_path"]],client:[[0,0,0,"-","client"],[0,0,0,"-","client_repository"]],common:[[1,0,0,"-","descriptor"],[1,0,0,"-","messages"],[1,0,0,"-","utils"],[1,0,0,"-","verifiers"]],pyqt_ui:[[3,0,0,"-","admin_page"],[3,0,0,"-","main"]],server:[[4,0,0,"-","repository"],[4,0,0,"-","server_utils"],[4,0,0,"-","utils"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","property","Python property"],"3":["py","method","Python method"],"4":["py","function","Python function"],"5":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:property","3":"py:method","4":"py:function","5":"py:attribute"},terms:{"11":0,"15":0,"17":0,"19":0,"2":0,"200":[1,4],"202":1,"2022":0,"400":1,"401":1,"409":1,"425772":0,"500":1,"7777":0,"\u0430":1,"\u0430\u043d\u0430\u043b\u0438\u0437\u0430":4,"\u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430":1,"\u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430\u0445":1,"\u0430\u0443\u0442\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438":[0,4],"\u0431\u0430\u0437\u0435":3,"\u0431\u0430\u0437\u0443":3,"\u0431\u0430\u0437\u044b":0,"\u0431\u0430\u0439\u0442\u044b":1,"\u0431\u0435\u0440\u0435\u0442":0,"\u0431\u044d\u043a\u0435\u043d\u0434":0,"\u0432":[0,1,3],"\u0432\u0430\u043b\u0438\u0434\u0430\u0446\u0438\u0438":4,"\u0432\u043d\u0435":1,"\u0432\u043e\u0437\u0432\u0440\u0430\u0449\u0430\u0435\u0442":3,"\u0432\u0441\u0435":0,"\u0432\u0441\u0435\u0445":0,"\u0432\u044b\u0431\u0440\u0430\u0441\u044b\u0432\u0430\u0435\u0442\u0441\u044f":1,"\u0432\u044b\u0434\u0430\u0451\u0442":1,"\u0432\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u043e\u043c\u0443":3,"\u0432\u044b\u0437\u044b\u0432\u0430\u0435\u0442\u0441\u044f":0,"\u0432\u044b\u0445\u043e\u0434\u0430":0,"\u0434\u0430\u043d\u043d\u044b\u0445":[0,3],"\u0434\u0435\u043a\u043e\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f":1,"\u0434\u0435\u0441\u043a\u0440\u0438\u043f\u0442\u043e\u0440":1,"\u0434\u0435\u0441\u043a\u0440\u0438\u043f\u0442\u043e\u0440\u043e\u0432":1,"\u0434\u0438\u0430\u043f\u0430\u0437\u043e\u043d\u0430":1,"\u0434\u043b\u044f":[0,1,3,4],"\u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0438":3,"\u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f":[0,3,4],"\u0435\u0433\u043e":1,"\u0435\u0441\u043b\u0438":1,"\u0437\u0430":0,"\u0437\u0430\u0434\u0430\u043d\u043d\u043e\u0433\u043e":1,"\u0437\u0430\u0434\u0430\u0447\u0430\u043c\u0438":0,"\u0437\u0430\u0434\u0430\u0447\u0438":0,"\u0437\u0430\u0434\u0430\u0447\u0443":0,"\u0437\u0430\u0434\u0430\u0451\u0442\u0441\u044f":1,"\u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435":0,"\u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e\u0441\u0442\u044c":3,"\u0437\u0430\u043f\u0443\u0441\u043a\u0430\u0435\u0442":0,"\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435":1,"\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f":[1,4],"\u0438":[0,1,3],"\u0438\u0437":[0,4],"\u0438\u043d\u0438\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438":1,"\u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435":1,"\u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f":1,"\u0438\u0441\u0442\u043e\u0440\u0438\u0438":0,"\u0438\u0441\u0442\u043e\u0440\u0438\u044e":0,"\u0438\u0445":0,"\u043a\u0430\u0436\u0434\u043e\u0439":0,"\u043a\u043b\u0430\u0434\u0435\u0442":0,"\u043a\u043b\u0430\u0441\u0441":[0,3],"\u043a\u043b\u0430\u0441\u0441\u0430":[0,1],"\u043a\u043b\u0438\u0435\u043d\u0442\u0430":[0,1,4],"\u043a\u043b\u044e\u0447\u0430\u043c\u0438":1,"\u043a\u043d\u043e\u043f\u043a\u0438":3,"\u043a\u043d\u043e\u043f\u043a\u0443":0,"\u043a\u043e\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f":1,"\u043a\u043e\u043b\u043b\u0431\u0435\u043a\u043e\u043c":0,"\u043a\u043e\u043d\u0441\u0442\u0430\u043d\u0442\u044b":1,"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0430":[0,3,4],"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043e\u0432":[0,3,4],"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0443":[0,3],"\u043a\u043e\u043d\u0442\u0440\u043e\u043b\u0438\u0440\u0443\u0435\u0442":1,"\u043a\u043e\u0442\u043e\u0440\u044b\u0439":0,"\u043b\u043e\u0433\u0438\u043d\u0430":3,"\u043c\u0435\u0436\u0434\u0443":0,"\u043c\u0435\u0442\u0430\u043a\u043b\u0430\u0441\u0441":1,"\u043c\u0435\u0442\u0430\u043a\u043b\u0430\u0441\u0441\u043e\u0432":1,"\u043c\u0435\u0442\u043e\u0434":[0,3],"\u043c\u0435\u0442\u043e\u0434\u0430":1,"\u043c\u0435\u0442\u043e\u0434\u043e\u0432":1,"\u043c\u043e\u0434\u0443\u043b\u044c":[0,1,3,4],"\u043d\u0430":[0,1],"\u043d\u0430\u0436\u0430\u0442\u0438\u0438":0,"\u043d\u0430\u0436\u0430\u0442\u0438\u044f":3,"\u043d\u0430\u043b\u0438\u0447\u0438\u0435":1,"\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438":1,"\u043d\u0435\u0433\u043e":0,"\u043d\u043e\u0432\u043e\u0433\u043e":3,"\u043e\u0431\u043c\u0435\u043d\u0430":1,"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443":0,"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a":3,"\u043e\u0431\u0449\u0438\u0435":0,"\u043e\u0431\u044a\u0435\u043a\u0442":0,"\u043e\u0431\u044a\u0435\u043a\u0442\u043e\u0432":1,"\u043e\u043a\u043d\u0430":3,"\u043e\u043a\u043d\u043e":3,"\u043e\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u0442":0,"\u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439":[0,3],"\u043e\u0441\u043d\u043e\u0432\u043d\u0443\u044e":3,"\u043e\u0441\u043d\u043e\u0432\u043d\u044b\u043c\u0438":1,"\u043e\u0442":[0,4],"\u043e\u0442\u0432\u0435\u0442":0,"\u043e\u0442\u0432\u0435\u0442\u0430":[0,4],"\u043e\u0442\u0432\u0435\u0442\u044b":0,"\u043e\u0442\u0432\u0435\u0447\u0430\u0435\u0442":0,"\u043e\u0442\u0432\u0435\u0447\u0430\u044e\u0449\u0438\u0439":0,"\u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u0442":3,"\u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u044e\u0449\u0438\u0439":3,"\u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f":[0,3],"\u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c":0,"\u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438":1,"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f":0,"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0433\u043e":3,"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442":[0,1,3],"\u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0438\u0435":1,"\u043e\u0447\u0435\u0440\u0435\u0434\u0438":0,"\u043e\u0447\u0435\u0440\u0435\u0434\u044c":0,"\u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0438":0,"\u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0443":0,"\u043f\u043e":[1,3],"\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f":1,"\u043f\u043e\u043a\u0430":0,"\u043f\u043e\u043b\u0435\u0439":3,"\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u043d\u043e\u0439":0,"\u043f\u043e\u043b\u0443\u0447\u0430\u0435\u0442":0,"\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u0435":0,"\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f":[0,4],"\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u043d\u043e\u0433\u043e":3,"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f":[0,3],"\u043f\u043e\u0440\u0442\u0430":1,"\u043f\u043e\u0442\u043e\u043a":0,"\u043f\u0440\u0435\u0434\u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u043d\u044b\u0439":0,"\u043f\u0440\u0438":[0,3],"\u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f":3,"\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0435\u0442":1,"\u043f\u0440\u0438\u0451\u043c\u0430":1,"\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438":[0,3],"\u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u0442":3,"\u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u0430":1,"\u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0435":0,"\u0440\u0430\u0437\u0431\u0438\u0440\u0430\u0435\u0442":0,"\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438":[0,3,4],"\u0441":[0,3],"\u0441\u0432\u043e\u0439\u0441\u0442\u0432\u0430":0,"\u0441\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0439":0,"\u0441\u0432\u044f\u0437\u044b\u0432\u0430\u0435\u0442":0,"\u0441\u0435\u0440\u0432\u0435\u0440":0,"\u0441\u0435\u0440\u0432\u0435\u0440\u0430":[0,1,4],"\u0441\u0435\u0440\u0432\u0435\u0440\u043e\u043c":0,"\u0441\u0438\u0433\u043d\u0430\u043b\u0443":0,"\u0441\u043b\u043e\u0432\u0430\u0440\u044c":1,"\u0441\u043b\u043e\u0432\u0430\u0440\u044f":4,"\u0441\u043b\u043e\u0442":3,"\u0441\u043b\u0443\u0447\u0430\u0435":1,"\u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0449\u0438\u0439":0,"\u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f":[0,4],"\u0441\u043e\u043a\u0435\u0442\u0430":[0,1],"\u0441\u043e\u043a\u0435\u0442\u0435":1,"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435":3,"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435\u043c":0,"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439":[0,4],"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f":[0,1,3,4],"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f\u043c\u0438":1,"\u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f":[0,3],"\u0441\u043f\u0438\u0441\u043a\u0430":[0,3,4],"\u0441\u043f\u0438\u0441\u043a\u0435":3,"\u0441\u043f\u0438\u0441\u043a\u043e\u043c":3,"\u0441\u043f\u0438\u0441\u043e\u043a":3,"\u0441\u0442\u0430\u0440\u0442\u043e\u0432\u043e\u0433\u043e":3,"\u0441\u0442\u0430\u0440\u0442\u043e\u0432\u043e\u0435":3,"\u0441\u0443\u0449\u0435\u0441\u0442\u0432\u043e\u0432\u0430\u043d\u0438\u044f":0,"\u0442\u0430\u0431\u043b\u0438\u0446\u0435":0,"\u0442\u0430\u0431\u043b\u0438\u0446\u044b":0,"\u0442\u0430\u043a\u0436\u0435":1,"\u0442\u0435\u043a\u0443\u0449\u0435\u0433\u043e":3,"\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f":[0,3,4],"\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438":3,"\u0443\u0442\u0438\u043b\u0438\u0442\u044b":1,"\u0444\u043e\u0440\u043c\u043e\u0439":3,"\u0444\u043e\u0440\u043c\u0443":3,"\u0444\u043e\u0440\u043c\u044b":3,"\u0444\u0443\u043d\u043a\u0446\u0438\u044f":[1,4],"\u0446\u0435\u043b\u044b\u0445":1,"\u0447\u0430\u0442\u0430":3,"\u0447\u0430\u0442\u043e\u043c":3,"\u0447\u0438\u0441\u043b":1,"\u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0443":3,"\u044d\u0442\u0430\u043f\u0435":1,"\u044f\u0432\u043b\u044f\u044e\u0449\u0438\u0435\u0441\u044f":1,"class":[0,1,3,4],"enum":1,"new":[0,4],"return":[0,4],"static":3,"true":0,TO:1,The:[0,4],__stop:0,__task_queu:0,accept:[0,1,4],account:[1,4],account_nam:[0,1],accountform:3,action:1,add_contact:[0,1,4],add_contact_sign:3,add_contact_to_list:3,add_histori:4,add_us:4,address:0,admin:3,admin_pag:2,alert:1,an:1,ani:[0,4],argument:[0,4],attribut:[0,4],auth:0,authent:1,authenticatefieldnam:1,back:3,back_to_welcom:3,bad_request:1,base:[0,1,3,4],birthdat:[0,1,4],bool:0,call:[0,4],callback:0,cannot:[0,4],check_contact:0,client:[2,3],client_id:4,client_login:4,client_repositori:2,clientrepositori:0,clientrequestfieldnam:1,clientverifi:1,clsdict:1,clsname:1,code:4,common:2,config:3,conflict:1,connect:1,connect_to_chat:3,connect_to_messeng:4,connection_record:4,cont_list_sign:3,contact:[0,3,4],contact_id:4,contact_login:4,create_read_only_cel:3,create_respons:4,create_socket:0,d:4,date:0,datetim:0,dbapi_connect:4,decl_api:[0,4],del_contact:[0,1,4],del_contact_from_list:3,del_contact_sign:3,del_us:[3,4],descriptor:2,dict:[0,1,4],enumer:1,error:1,featureless:[0,4],from:1,from_acc:0,get_all_user_histori:4,get_config:4,get_config_path:4,get_contact:[1,4],get_contact_list:0,get_data:1,get_hash:4,get_message_histori:0,get_us:4,get_user_histori:4,given:[0,4],go_to_login:3,ha:[0,4],handle_contacts_respons:3,hierarchi:[0,4],histori:4,id:0,index:[2,3],instanc:[0,4],internal_server_error:1,ip_address:4,jim:1,kei:4,kwarg:[0,4],list:4,listen:[0,1],load_server_set:3,load_stat:3,load_us:[3,4],localhost:0,logger:1,login:[0,1,3,4],login_sign:3,login_tim:4,loginform:3,logout:0,lst:4,main:2,messag:[0,2,3],message_receiv:3,message_s:3,message_sent_sign:3,messagehistori:0,messagetyp:1,metadata:[0,4],modul:2,msg:[0,1,3,4],msgfieldnam:1,multi_serv:2,mycontact:0,name:[0,1,4],none:[3,4],obj:4,object:[0,1,4],ok:1,orm:[0,4],owner:4,owner_login:4,packag:2,page:2,param:0,pass_hash:4,password:[0,1,4],password_hash:4,port:[0,1],presenc:[0,1,4],properti:0,pyqt5:3,pyqt_ui:2,qdialog:3,qmainwindow:3,qtwidget:3,queue:0,receive_message_sign:3,receiverthread:0,recipient_nam:0,registri:[0,4],remove_contact:3,remove_from_list:4,remove_if_pres:4,repositori:2,requesttoserv:1,respons:[1,3],responsecod:1,responses_queu:0,result:0,result_callback:0,run:0,salt:4,save_messag:0,save_server_set:3,search:2,send:[0,3],send_btn_click:3,send_messag:1,senderthread:0,sendtask:0,server:2,server_util:2,serverresponsefieldnam:1,serververifi:1,set_current_chat:3,set_sqlite_pragma:4,show_account_form:3,show_file_dialog:3,show_new_contact:3,sign_up:[0,1,3,4],sign_up_for_messeng:3,sign_up_sign:3,signupform:3,sock:[0,1],socket:0,sqlalchemi:[0,4],stop:0,str:[0,4],submit_task:0,submodul:2,subscribe_to_messag:0,surnam:[0,1,4],tab_chang:3,task:0,tcp:1,text:3,thread:0,time:1,to_acc:0,type:1,ui:[0,3],unauthor:1,url:[0,4],user:[1,4],user_id:1,user_login:1,userfieldnam:1,userhistori:4,util:2,validate_add_contact:4,validate_authent:4,validate_del_contact:4,validate_get_contact:4,validate_pres:4,validate_sign_up:4,validate_user_msg:4,valu:1,verifi:2,welcom:3,welcomeform:3,when:[0,4]},titles:["client package","common package","Welcome to Messenger\u2019s documentation!","pyqt_ui package","server package"],titleterms:{admin_pag:3,client:0,client_repositori:0,common:1,content:[0,1,2,3,4],descriptor:1,document:2,indic:2,main:3,messag:1,messeng:2,modul:[0,1,3,4],multi_serv:4,packag:[0,1,3,4],pyqt_ui:3,repositori:4,s:2,server:4,server_util:4,submodul:[0,1,3,4],tabl:2,util:[1,4],verifi:1,welcom:2}})