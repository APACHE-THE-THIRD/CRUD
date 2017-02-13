import wx
import wx.lib.mixins.listctrl  as  listmix
import sqllite

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):


    # ----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):

        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

class MyPanel(wx.Panel):


    # ----------------------------------------------------------------------
    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        self.db_connector = sqllite.sqlite3_connector()


        fgs_main = wx.FlexGridSizer(5, 2, 10, 10)

        self.add_bttn = wx.Button(self, label="Add")
        self.add_bttn.Bind(wx.EVT_BUTTON, self.on_add_bttn)

        self.list_ctrl = EditableListCtrl(self, style= wx.LC_REPORT)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_remove)

        self.list_ctrl.InsertColumn(0, "ID")
        self.list_ctrl.InsertColumn(1, "NAME")
        self.list_ctrl.InsertColumn(2, "SURNAME")
        self.list_ctrl.InsertColumn(3, "TASK")

        self.update_list_from_db()
        hbox = wx.BoxSizer(wx.HORIZONTAL)


        fgs_edit = wx.FlexGridSizer(5, 2, 10, 10)
        hbox_bttns = wx.BoxSizer(wx.HORIZONTAL)

        self.id_lbl = wx.StaticText(self, -1, "ID:  ")
        self.id_text_field = wx.TextCtrl(parent=self, name="id", style=wx.TE_READONLY)

        self.name_lbl = wx.StaticText(self, -1, "NAME:  ")
        self.name_text_field = wx.TextCtrl(parent=self, name="Name")

        self.surname_lbl = wx.StaticText(self, -1, "SURNAME:  ")
        self.surname_text_field = wx.TextCtrl(parent=self, name="Surname")

        self.task_lbl = wx.StaticText(self, -1, "TASK:  ")
        self.task_text_field = wx.TextCtrl(parent=self, name="Task")

        self.save_bttn = wx.Button(self, label="Save")
        self.save_bttn.Disable()
        self.save_bttn.Bind(wx.EVT_BUTTON, self.on_save)
        self.cancel_bttn = wx.Button(self, label="Clear")
        self.cancel_bttn.Bind(wx.EVT_BUTTON, self.on_clear)
        hbox_bttns.AddMany([self.save_bttn, self.cancel_bttn])

        fgs_edit.AddMany(([self.id_lbl, self.id_text_field, self.name_lbl, self.name_text_field, self.surname_lbl, self.surname_text_field,
                      self.task_lbl, self.task_text_field, self.save_bttn, self.cancel_bttn]))
        hbox.Add(fgs_edit)

        fgs_main.AddMany([self.list_ctrl, hbox, self.add_bttn])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(fgs_main, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)

    def update_list_from_db(self):
        self.list_ctrl.DeleteAllItems()
        records = self.db_connector.select_all()
        for i,row in enumerate(records):
            self.list_ctrl.InsertItem(i, str(row[0]))
            self.list_ctrl.SetItem(i, 1, str(row[1]))
            self.list_ctrl.SetItem(i, 2, str(row[2]))
            self.list_ctrl.SetItem(i, 3, str(row[3]))


    def on_add_bttn(self, event):
        index =  self.list_ctrl.GetItemCount()
        max_id = self.db_connector.get_max_task_id()
        self.db_connector.insert_one(max_id + 1, "name", "surname", "task")
        self.update_list_from_db()


    def on_remove(self, event):
        index = self.list_ctrl.GetFirstSelected()
        db_index = int(self.list_ctrl.GetItemText(index))
        self.db_connector.delete_one(db_index)

        self.update_list_from_db()

    def on_item_selected(self, event):
        self.save_bttn.Enable()
        gui_index = event.GetIndex()
        db_index = int(self.list_ctrl.GetItemText(gui_index))
        item_data =[]
        for column in range(self.list_ctrl.GetColumnCount()):
            item_data.append(self.list_ctrl.GetItemText(gui_index, column))

        self.id_text_field.SetValue(item_data[0])
        self.name_text_field.SetValue(item_data[1])
        self.surname_text_field.SetValue(item_data[2])
        self.task_text_field.SetValue(item_data[3])

    def on_save(self, event):
        id = self.id_text_field.GetValue()
        name = self.name_text_field.GetValue()
        surname = self.surname_text_field.GetValue()
        task = self.task_text_field.GetValue()

        self.db_connector.update_one(int(id), name, surname, task)
        self.update_list_from_db()


    def on_clear(self, event):
        self.save_bttn.Disable()
        id = self.id_text_field.Clear()
        name = self.name_text_field.Clear()
        surname = self.surname_text_field.Clear()
        task = self.task_text_field.Clear()

class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "sqlite3 crud", size=(600, 250))
        panel = MyPanel(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()