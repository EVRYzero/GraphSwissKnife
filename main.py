from debug.exceptions import CustomException
from ui.ui import UI

ui = UI()

while True:
    try:
        ui.main_menu()
        user_choice = input("Choice: ")
        if user_choice == "0":
            break
        elif user_choice == "1":
            ui.get_vertices_number()
        elif user_choice == "2":
            ui.get_vertices()
        elif user_choice == "3":
            ui.get_in_degree_of_vertex()
        elif user_choice == "4":
            ui.get_out_degree_of_vertex()
        elif user_choice == "5":
            ui.get_inbound_edges_of_vertex()
        elif user_choice == "6":
            ui.get_outbound_edges_of_vertex()
        elif user_choice == "7":
            ui.add_vertex()
        elif user_choice == "8":
            ui.delete_vertex()
        elif user_choice == "9":
            ui.add_edge()
        elif user_choice == "10":
            ui.delete_edge()
        elif user_choice == "11":
            ui.modify_edge_cost()
        elif user_choice == "12":
            ui.check_edge()
        elif user_choice == "13":
            ui.import_templated_graph()
        elif user_choice == "14":
            ui.generate_graph()
        elif user_choice == "15":
            ui.import_exported_graph()
        elif user_choice == "16":
            ui.export_graph()
        elif user_choice == "17":
            ui.copy_graph()
        elif user_choice == "18":
            ui.get_connected_components_of_graph()
        elif user_choice == "19":
            ui.lowest_cost()
        elif user_choice == "20":
            ui.minimal_spanning_tree()
        elif user_choice == "21":
            ui.hamiltonian_cycle_of_low_cost()
        else:
            pass
    except CustomException as exception:
        print(str(exception))
