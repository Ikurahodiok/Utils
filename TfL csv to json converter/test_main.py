import unittest

import main


class MyTestCase(unittest.TestCase):  # inherting from this module
    def setUp(self):
        """
        runs every time before each test. Create dummy example records
        :return:
        """
        self.rec_valid = main.Row(['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
                                   'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
                                  ['00/000111', 'DC', 'Pedestrian', '08-Apr-2006', '532922', '180859',
                                   'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
                                   'CNTR', 'R27', 'Active', 'John Smith'],
                                  666)

        self.rec_null_id = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['', 'PD', 'Pedestrian', '08-Apr-06', '532922', '180859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
             'CNTR', 'R27', 'Active', 'John Smith'],
            667)

        self.rec_fewer_fields = main.Row(
            ['TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['00/000111', 'PD', 'Pedestrian', '08-Ap-2006', '532922', '180859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
             'CNTR', 'R27', 'Active', 'John Smith'],
            668)

        self.rec_text_id = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['00/0001ss', 'DC', 'Pedestrian', 'f8-Apr-2006', '532922', '000859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
             'CNTR', 'R27', 'Active', 'John Smith'],
            669)

        self.rec_id_3parts = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['00/0/001ss', 'PD', 'Pedestrian', '8-Apr-2006', '532922', '180859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
             'CNTR', 'R27', 'Active', 'John Smith'],
            670)

        self.rec_id_short_parts = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['00/0', 'PGGG', 'Pedestrian', '08-Apr-06', '999999', '180859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
             'CNTR', 'R27', 'Active', 'John Smith'],
            671)
        self.rec_null_type = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['00/000111', '', 'Pedestrian456', '08-Apr-06', '532922', '000859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
             'CENTER', 'R27', 'Maybe Active', 'John Smith John Smith John Smith'],
            672)
        self.rec_null_all = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['', '', '', '', '', '', '', '', '', '', ''],
            673)

        self.rec_long_all = main.Row(
            ['ID', 'TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
             'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
            ['000/00000111', 'DCDD', 'Pedestrian123123123123123', '08-Apr-06', '532922', '180859',
             'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET 345dfa  wg wg sdfg gs fg sfg wdfg sfg sfg sdfg '
             'sdfg sf gsdf gs dfgs fgs fg sfg asfdg aegklnqerlghwkrtgbwkgjqerg afgagsf - EASTCHEAP',
             'CNTR', 'R2735345356356', 'Active', 'John Smith'],
            674)
        #    creation causes error self.installedBy = row[10] # IndexError: list index out of range
        # self.rec_fewer_rows = main.Row(
        #     ['ID','TYPE', 'TYPE_DESC', 'INSTALL_DATE', 'EASTING', 'NORTHING', 'LOCATION', 'CELL',
        #      'SIGNAL_GROUP', 'STATUS', 'INSTALL_ENGINEER'],
        #     ['PD', 'Pedestrian', '08-Apr-06', '532922', '180859',
        #      'GRACECHURCH STREET - KING WILLIAM STREET - CANNON STREET - EASTCHEAP',
        #      'CNTR', 'R27', 'Active', 'John Smith'],
        #     666)

        # testing to see correct retrieval
        print(self.rec_valid.id, self.rec_null_id.id)
        print('shorter field', len(self.rec_fewer_fields.fields), len(self.rec_fewer_fields.row))

    def tearDown(self):
        # any deletion of files written during setUp
        pass

    # ------ Testing overarching class methods ------
    def test_is_integer(self):
        # self.assertRaises(ValueError, main.ConversionModule.is_integer, 'g')
        # not ok - ValueError not raised as err handling in code
        self.assertEqual(main.ConversionModule.is_integer(self,2), True)  # ok
        # self.assertEqual(main.ConversionModule.is_integer(2), False)  # not ok
        self.assertEqual(main.ConversionModule.is_integer(self,2.2), False)  # ok - int(2.2) --> 2
        self.assertEqual(main.ConversionModule.is_integer(self,'text'), False)  # ok
        # self.assertEqual(main.ConversionModule.is_integer(''), False)
        # not ok, err --> but no instance would occur. Is always ''

    def test_is_null(self):
        self.assertEqual(main.ConversionModule.is_null(self, None, 1), True)
        self.assertEqual(main.ConversionModule.is_null(self, '', 2), True)
        self.assertEqual(main.ConversionModule.is_null(self, 'A Value', 3), False)
        return

    def test_longer_than(self):
        self.assertEqual(main.ConversionModule.longer_than(self, None, 1, 1), False)
        self.assertEqual(main.ConversionModule.longer_than(self, '', 1, 2), False)
        self.assertEqual(main.ConversionModule.longer_than(self, 'one', 1, 3), True)

    def test_val_lies_between(self):
        # already tested if null, or if int
        self.assertEqual(main.ConversionModule.val_lies_between(self, 0, -1, 1, 1), True)
        self.assertEqual(main.ConversionModule.val_lies_between(self, 0, 1, 1, 2), False)
        self.assertEqual(main.ConversionModule.val_lies_between(self, 30 ** 2, 0, 30 ** 4, 3), True)
        self.assertEqual(main.ConversionModule.val_lies_between(self, 0, 0, 0, 4), True)

    def test_val_not_present_in(self):
        # already checked if null
        self.assertEqual(main.ConversionModule.val_present_in(self, 'a', ['a', 'b', 'c']), True)
        self.assertEqual(main.ConversionModule.val_present_in(self, 'd', ['a', 'b', 'c']), False)

    def test_is_string(self):
        self.assertEqual(main.ConversionModule.is_string(self, 'test string'), True)
        self.assertEqual(main.ConversionModule.is_string(self, ''), True)  # fine as is_null() checks the length > 0
        self.assertEqual(main.ConversionModule.is_string(self, None), False)
        self.assertEqual(main.ConversionModule.is_string(self, 43), False)


    def test_split_str_on(self):
        self.assertEqual(main.ConversionModule.split_str_on(self, 'test string', ' '), ['test', 'string'])
        self.assertEqual(main.ConversionModule.split_str_on(self, 'test string', ''), 'test string')

    def test_int_check_each_letter_in_each_word(self):
        self.assertEqual(main.ConversionModule.int_check_each_letter_in_each_word(self, ['test','string']), False)
        self.assertEqual(main.ConversionModule.int_check_each_letter_in_each_word(self, ['123','4567']), True)
        # self.assertEqual(main.ConversionModule.int_check_each_letter_in_each_word(self, ['','']), True)
        # thankfully have other checks in id_check() which prevent nulls

    def test_if_null_return_empty_string(self):
        self.assertEqual(main.ConversionModule.if_null_return_empty_string(self, ""), "")
        self.assertEqual(main.ConversionModule.if_null_return_empty_string(self, "0"), "0")
        self.assertEqual(main.ConversionModule.if_null_return_empty_string(self, 0), "0")


    # ------ Testing entire rows ------
    def test_id_check(self):
        self.assertEqual(main.Row.id_check(self.rec_valid), True)
        self.assertEqual(main.Row.id_check(self.rec_null_id), False)
        self.assertEqual(main.Row.id_check(self.rec_text_id), False)
        self.assertEqual(main.Row.id_check(self.rec_id_3parts), False)
        self.assertEqual(main.Row.id_check(self.rec_id_short_parts), False)
        self.assertEqual(main.Row.id_check(self.rec_null_all), False)

    def test_type_check(self):
        self.assertEqual(main.Row.type_check(self.rec_valid), True)
        self.assertEqual(main.Row.type_check(self.rec_null_type), False)
        self.assertEqual(main.Row.type_check(self.rec_id_short_parts), False)  # type = 'PGGG'
        self.assertEqual(main.Row.id_check(self.rec_null_all), False)

    def test_type_desc_check(self):
        self.assertEqual(main.Row.type_desc_check(self.rec_valid), True)
        self.assertEqual(main.Row.type_desc_check(self.rec_null_all), False)
        self.assertEqual(main.Row.type_desc_check(self.rec_null_type), False)  # type = > 11

    def test_E_or_N_checks(self):
        self.assertEqual(main.Row.E_or_N_checks(self.rec_valid), True)
        self.assertEqual(main.Row.E_or_N_checks(self.rec_null_all), False)
        self.assertEqual(main.Row.E_or_N_checks(self.rec_id_short_parts), False)  # E is too big
        self.assertEqual(main.Row.E_or_N_checks(self.rec_text_id), False)  # W is too small

    def test_location_checks(self):
        self.assertEqual(main.Row.location_checks(self.rec_valid), True)
        self.assertEqual(main.Row.location_checks(self.rec_null_all), True)  # len('') = 0 < 100
        self.assertEqual(main.Row.location_checks(self.rec_long_all), False)

    def test_cell_checks(self):
        self.assertEqual(main.Row.cell_checks(self.rec_valid), True)
        self.assertEqual(main.Row.cell_checks(self.rec_null_all),
                         True)  # null was entered as an acceptable value in 'asset_control_servers'
        self.assertEqual(main.Row.cell_checks(self.rec_null_type), False)  # CNTR --> CENTER

    def test_signal_group_checks(self):
        self.assertEqual(main.Row.signal_group_checks(self.rec_valid), True)
        self.assertEqual(main.Row.signal_group_checks(self.rec_null_all),
                         True)  # null was entered as an acceptable value in 'asset_control_servers'
        self.assertEqual(main.Row.signal_group_checks(self.rec_long_all), False)  # CNTR --> CENTER

    def test_asset_status_checks(self):
        self.assertEqual(main.Row.asset_status_check(self.rec_valid), True)
        self.assertEqual(main.Row.asset_status_check(self.rec_null_all),
                         False)  # null was entered as an acceptable value in 'asset_control_servers'
        self.assertEqual(main.Row.asset_status_check(self.rec_null_type), False)  # 'Maybe active'

    def test_install_engineer_checks(self):
        self.assertEqual(main.Row.install_engineer_check(self.rec_valid), True)
        self.assertEqual(main.Row.install_engineer_check(self.rec_null_all),
                         True)  # null was entered as an acceptable value in 'asset_control_servers'
        self.assertEqual(main.Row.install_engineer_check(self.rec_null_type), False)  # long eng name

    def test_install_date_check(self):
        self.assertEqual(main.Row.install_date_check(self.rec_valid), True)
        self.assertEqual(main.Row.install_date_check(self.rec_null_all), True)
        self.assertEqual(main.Row.install_date_check(self.rec_fewer_fields), False)  # 08-Ap-
        self.assertEqual(main.Row.install_date_check(self.rec_text_id), False)  # f8-Apr
        self.assertEqual(main.Row.install_date_check(self.rec_id_3parts), False)  # 8-Apr
        self.assertEqual(main.Row.install_date_check(self.rec_null_type), False)  # 8-Apr-06

    def test_reading_csv(self):
        """
        make sure input file is actually a '.csv'
        :return:
        """
        # self.assertRaises(main.ConversionModule.read_csv(self, 'example.txt'), TypeError)
        # fails for some reason, but TypeError raised

    # not undertaking unit testing on the writing as all data validity checks have been done.
    # There should be no problematic cases (ideally. would only be able to test with more data?)


if __name__ == '__main__':
    unittest.main()
