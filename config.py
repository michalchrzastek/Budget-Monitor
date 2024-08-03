import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+ os.getcwd() +"/budgetmonitor.db"
    DOWNLOADED_STATEMENT = os.path.join('/Users',os.environ['USER'],'Downloads')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 15
    ALLOWED_EXTENSIONS = set(['qif'])
    CHART_1_MONTH_COUNT = 6
    CHART_2_MONTH_COUNT = 12
    CHART_3_MONTH_COUNT = 12
    FUEL_TAG_NAME = 'CarFuel'
    CURRENCY_SYMBOL = '£'
    LOCAL_LANG = "en"
    LOCAL_DICT = {
        "en":{
            "budget_monitor":"Budget Monitor",
            "tools":"Tools",
            "new_acc_name":"New Account Name",
            "tag_groups":"Tag Groups",
            "tags":"Tags",
            "conditions":"Conditions",
            "descriptions":"Descriptions",
            "balance":"Balance",
            "last_upload":"Last Upload",
            "view":"View",
            "confirm_delete":"Confirm Delete",
            "delete_acc_msg1":"Are you sure you want to delete this account and all associated data?",
            "delete_acc_msg2":"This cannot be reversed!",
            "delete":"Delete",
            "close":"Close",
            "all":"All",
            "new":"New",
            "upload_statement":"Upload Statement",
            "overview":"Overview",
            "month_arr":"Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec",
            "chrt_lbl_months":"months",
            "chrt_lbl_monthly_trend_in_out":"Monthly Trend (In vs Out)",
            "chrt_lbl_summary_table":"Summary Table",
            "chrt_lbl_monthdays":"Transactions By Month Day",
            "chrt_lbl_detail":"Details by Month",
            "chrt_lbl_timeline":"Trend Timeline",
            "chrt_lbl_fuel":"Fuel Trend",
            "chrt_lbl_litres":"Litres",
            "chrt_lbl_miles":"Miles",
            "chrt_lbl_cost":"Cost",
            "category":"Category",
            "count":"Transaction Count",
            "total":"Total Amount",
            "avg":"Avg Transaction",
            "prev_year":"Prev Year",
            "ytd":"YTD",
            "avg_month":"Avg Month",
            "prev_month":"Prev Month",
            "msg_no_trans":"No transactions, please upload a statement.",
            "msg_select_stmt_file":"Select Statement File",
            "msg_update_amount":"Update amount of the original transaction to",
            "flash_msg_new_account_created":"New Account Has Been Created",
            "flash_msg_account_deleted":"The Account Has Been Deleted",
            "flash_msg_wrong_file":"This file type is not accepted, must be a *.qif statement",
            "flash_msg_stmt_uploaded":"Statement uploaded, ",
            "flash_msg_found":"Found",
            "flash_msg_saved":"Saved",
            "flash_msg_transaction_updated":"Transaction Updated",
            "flash_msg_transaction_created":"New Transaction Created",
            "flash_msg_transaction_deleted":"Transaction deleted",
            "flash_msg_condition_created":"New Condition Created",
            "flash_msg_condition_updated":"Condition Updated",
            "flash_msg_condition_deleted":"Condition Removed",
            "flash_msg_no_more_trans":"No More New Transactions To Edit",
            "flash_msg_no_tag_selected":"At Least 1 TAG Must Be Selected. Found NONE, Selected ALL",
            "flash_msg_descr_updated":"Description updated",
            "flash_msg_descr_created":"New description created",
            "flash_msg_descr_deleted":"Description deleted",
            "flash_msg_descr_trans_updated":"Matching Text Replaced",
            "flash_msg_group_updated":"Group Updated",
            "flash_msg_group_created":"New Group And Tag Created",
            "flash_msg_group_deleted":"Group Deleted",
            "flash_msg_tag_updated":"Tag Updated",
            "flash_msg_tag_created":"New Tag Created",
            "flash_msg_tag_deleted":"Tag Deleted",
            "title_all_transactions":"All Transactions",
            "title_new_transactions":"New Transactions",
            "title_account_summary":"Account Summary",
            "title_tag_conditions":"Tag Conditions",
            "title_change_transaction_description":"Change Transaction Description",
            "title_tag_groups":"Tag Groups",
            "title_tags":"Tags",
            "credit":"Credit",
            "debit":"Debit",
            "card":"Card",
            "transaction":"Transaction",
            "date":"Date",
            "amount":"Amount",
            "upload":"Upload",
            "from":"Date Range From",
            "to":"Date Range To",
            "transaction_text_to_match":"Transaction Text To Match",
            "replace_from":"Replace From",
            "replace_to":"Replace To",
            "original_text":"Original Transaction Text",
            "new_text":"New Text",
            "tag_group_name":"Tag Group Name",
            "group_color":"Group Color",
            "tag_name":"Tag Name",
            "tag_group":"Tag Group",
            "incl_summary":"Include in Summary",
            "chart":"Chart",
            "split":"SPLIT",
            "btn_apply_filter":"Apply Filter",
            "btn_reset_filter":"Reset Filter",
            "btn_save":"Save Changes",
            "btn_create_match_string":"Create Match String",
            "btn_split_transaction":"Split Transaction",
            "btn_delete":"Delete",
            "btn_create":"Create",
            "btn_rename_matching":"Rename Matching",
            "btn_tags_select":"Select All Tags",
            "btn_tags_unselect":"Unselect All Tags",
            "btn_show_more":""
            },
        "pl":{
            "budget_monitor":"Budget Monitor",
            "tools":"Ustawienia",
            "new_acc_name":"Nazwa Nowego Konta",
            "tag_groups":"Grupy",
            "tags":"Kategorie",
            "conditions":"Domyślne Kategorie",
            "descriptions":"Skróć Opis",
            "balance":"Stan Konta",
            "last_upload":"Poprzedni wrzut",
            "view":"Wejdź",
            "confirm_delete":"Potwierdź Usunięcie",
            "delete_acc_msg1":"Czy na pewno chcesz usunąć to konto oraz wszystkie dane?",
            "delete_acc_msg2":"Tego nie można odwrócić!",
            "delete":"Usuń",
            "close":"Zamknij",
            "all":"Wszystkie Tranzakcje",
            "new":"Nowe Tranzakcje",
            "upload_statement":"Wrzuć Wykaz",
            "overview":"Przegląd",
            "month_arr":"Sty,Lut,Mar,Kwi,Maj,Cze,Lip,Sie,Wrz,Paź,Lis,Gru",
            "chrt_lbl_months":"miesięcy",
            "chrt_lbl_monthly_trend_in_out":"Tręd Miesięczny (w kontraście)",
            "chrt_lbl_summary_table":"Podsumowanie",
            "chrt_lbl_monthdays":"Tranzakcje Dzień Miesiąca",
            "chrt_lbl_detail":"Wykres Miesięczny",
            "chrt_lbl_timeline":"Trend Na Osi Czasu",
            "chrt_lbl_fuel":"Wykres Paliwa",
            "chrt_lbl_litres":"Litrów",
            "chrt_lbl_miles":"Mil",
            "chrt_lbl_cost":"Koszt",
            "category":"Kategoria",
            "count":"Liczba Tranzakcji",
            "total":"Kwota Całkowita",
            "avg":"Średnia Tranzakcja",
            "prev_year":"Poprzedni Rok",
            "ytd":"Kwota Roczna",
            "avg_month":"Przeciętny Miesiąc",
            "prev_month":"Poprzedni Miesiąc",
            "msg_no_trans":"Brak tranzakcji. Proszę wrzucić wykaz.",
            "msg_select_stmt_file":"Wybierz plik z wykazem",
            "msg_update_amount":"Zaktualizuj kwotę pierwotnej transakcji do",
            "flash_msg_new_account_created":"Nowe Konto Zostało Utworzone",
            "flash_msg_account_deleted":"Konto Zostało Usunięte",
            "flash_msg_wrong_file":"Błędne Rozszerzenie Pliku. Wykaz Powinien Być Typu *.qif",
            "flash_msg_stmt_uploaded":"Wykaz Zczytany, ",
            "flash_msg_found":"Wykryto",
            "flash_msg_saved":"Zapisano",
            "flash_msg_transaction_updated":"Tranzakcja Zaktualizowana",
            "flash_msg_transaction_created":"Utworzono Nową Tranzakcję",
            "flash_msg_transaction_deleted":"Tranzakcja Została Usunięta",
            "flash_msg_condition_created":"Utworzono Nową Domyślną Kategorię",
            "flash_msg_condition_updated":"Zaktualizowano Domyślną Kategorię",
            "flash_msg_condition_deleted":"Usunięto Domyślną Kategorię",
            "flash_msg_no_more_trans":"Wszystkie Nowe Tranzakcje Zostały Zaktualizowane",
            "flash_msg_no_tag_selected":"Brak Zaznaczonej Kategorii. Wymagana Liczba To 1. Automatycznie Zaznaczono Wszytkie",
            "flash_msg_descr_updated":"Opis Zaktualizowany",
            "flash_msg_descr_created":"Nowy Opis Utworzony",
            "flash_msg_descr_deleted":"Opis Usunięty",
            "flash_msg_descr_trans_updated":"Tranzakcje Zaktualizowe Nowym Opisem",
            "flash_msg_group_updated":"Groupa Zaktualizowana",
            "flash_msg_group_created":"Utworzono Nową Grupę Oraz Kategorię",
            "flash_msg_group_deleted":"Usunięto Grupę",
            "flash_msg_tag_updated":"Kategoria Zaktualizowana",
            "flash_msg_tag_created":"Utworzono Nową Kategorię",
            "flash_msg_tag_deleted":"Kategoria Usunięta",
            "title_all_transactions":"Wszystkie Tranzakcje",
            "title_new_transactions":"Nowe Tranzakcje",
            "title_account_summary":"Podsumowanie Konta",
            "title_tag_conditions":"Domyślne Kategorie",
            "title_change_transaction_description":"Zmień Opis Tranzakcji",
            "title_tag_groups":"Grupy Kategorii",
            "title_tags":"Kategorie",
            "credit":"Karta Kredytowa",
            "debit":"Karta Debetowa",
            "card":"Karta",
            "transaction":"Tranzakcja",
            "date":"Data",
            "amount":"Kwota",
            "upload":"Wrzuć",
            "from":"Od Daty",
            "to":"Do Daty",
            "transaction_text_to_match":"Znajdź Opis Tranzakcji",
            "replace_from":"Zamień z",
            "replace_to":"Zamień na",
            "original_text":"Wstępny Opis Tranzakcji",
            "new_text":"Nowy Opis",
            "tag_group_name":"Nazwa Grupy Kategorii",
            "group_color":"Kolor Grupy",
            "tag_name":"Nazwa Kategorii",
            "tag_group":"Grupa Kategorii",
            "incl_summary":"Podsumowanie",
            "chart":"Wykres",
            "split":"PODZIELONO",
            "btn_apply_filter":"Zastosuj Filtr",
            "btn_reset_filter":"Resetuj Filtr",
            "btn_save":"Zapisz",
            "btn_create_match_string":"Utwórz Domyślną Kategorię",
            "btn_split_transaction":"Podziel Tranzakcję",
            "btn_delete":"Usuń",
            "btn_create":"Utwórz",
            "btn_rename_matching":"Zamień Istniejące Opisy",
            "btn_tags_select":"Zaznacz Wszystkie Kategorie",
            "btn_tags_unselect":"Odznacz Wszytskie Kategorie",
            "btn_show_more":"Pokaż Więcej"
            }
    }