import os

from visualization_utils import bar_graphs_characters, print_length_stats_latex, bar_graphs_ch
from stats import stats_on_numbers
from visualization_morphemes import bar_graphs_morphemes
from visualization_ety_types import ety_types, ety_types_table_pl, ety_types_bar_graph_normalized
from visualization_depths import number_of_depths
from visualization_influence import print_page_rank_data

os.system('clear')

# -------------------------------
# ------- VISUALIZATION ---------
# -------------------------------


print("visualizing...")

# number of characters per set
# bar_graphs_characters("ALL")
# bar_graphs_characters("PL")
# bar_graphs_characters("CP")
# bar_graphs_characters("RG")
# bar_graphs_characters("PM")

# noc_all = stats_on_numbers("All", "name_length", "Number of Characters")
# noc_pl = stats_on_numbers("PL", "name_length", "Number of Characters")
# noc_cp = stats_on_numbers("CP", "name_length", "Number of Characters")
# noc_rg = stats_on_numbers("RG", "name_length", "Number of Characters")
# noc_pm = stats_on_numbers("PM", "name_length", "Number of Characters")

# number morphemes per set
# bar_graphs_morphemes("ALL")
# bar_graphs_morphemes("PL")
# bar_graphs_morphemes("CP")
# bar_graphs_morphemes("RG")
# bar_graphs_morphemes("PM")


# statistical data on mophemes per set
# nom_all = stats_on_numbers("All", "morpheme", "Number of Morphemes")
# nom_pl = stats_on_numbers("PL", "morpheme", "Number of Morphemes")
# nom_cp = stats_on_numbers("CP", "morpheme", "Number of Morphemes")
# nom_rg =  stats_on_numbers("RG", "morpheme", "Number of Morphemes")
# nom_pm = stats_on_numbers("PM", "morpheme", "Number of Morphemes")
# nom_top = stats_on_numbers("TOP", "morpheme", "Number of Morphemes")
# print_length_stats_latex([nom_all, nom_pl, nom_cp, nom_rg, nom_pm, nom_top], ["All", "PL", "CP", "RG", "PM", "TOP"])

# etymological depths
# number_of_depths("ety_depths") # defaults to all
# number_of_depths("ety_depths", "PL")
# number_of_depths("ety_depths", "CP")
# number_of_depths("ety_depths", "RG")
# number_of_depths("ety_depths", "PM")

# ety types per decade
# ety_types('ety_type_1_by_decade')
# ety_types('ety_type_2_by_decade')

# stats on ety types
# ety_types_table_pl('ety_type_2_by_decade')
# ety_types_bar_graph_normalized()
# ety_types('ety_type_2_by_decade', normalized=True)
# ety_types_table_pl('ety_type_2_by_decade')

# page rank data
# print_page_rank_data('ALL')
print_page_rank_data('PL')
print_page_rank_data('CP')
print_page_rank_data('RG')
print_page_rank_data('PM')

# cultural heritage
# bar_graphs_ch() # "CH", 'cultural_heritage'

# version numbering
# version_numbering("All")