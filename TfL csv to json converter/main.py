# ###############################################################################
# Script Name: Main.py
# Description: Read .csv's and convert to .json format and write to .json
# Arguments: 'Sample Data.csv'
# Output: 'Sample Data.json', 'Sample Data Invalid.csv'
# Author: Christopher Koido-Bunt
# ################################################################################

# global variables - here so test_main.py can access them
file_name = 'Sample Data.csv'
n_id_parts = 2  # ID = 'part1' / 'part2'
id_len = 9
asset_type_codes = ['DC', 'MP', 'P', 'PD', 'TN']
type_desc_length = 11
location_length = 100
n_coord_ref = 6  # six fig grid ref
mbr = [500000, 560000, 150000, 200000]  # East min, East max, North Min, North Max
asset_control_servers = ['CNTR', 'EAST', 'NORT', 'OUTR', 'SOUT', '']  # '' allows Null, bit hacky
sig_gr_char_len = 5
asset_statuses = ['Active', 'Proposed']
engineer_char_length = 15
len_date_parts = (2, 3, 4)  # dd-MMM-yyyy
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_text_to_numeric = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                         'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


class ConversionModule:
    def __init__(self,):
        """
        initialise the overarching conversion module class
        """

    def read_csv(self, file_name_):
        """
        Reads in the csv into a header list and a list of lists for data
        :param file_name - name of file in same directory as this script
        :return: 'fields' list and 'data' lists of lists
        """
        if file_name_[-4:] != '.csv':
            raise TypeError("The input file does not end with '.csv', no guarantee converter module will work")

        with open(file_name_, 'r') as f:
            data_ = []
            count = 0
            for line in f:
                line = line.replace('\n', '')  # rm
                # print(line)
                if count == 0:
                    fields = line.split(',')  # create: one-off for header
                if count > 0:
                    data_.append(line.split(','))
                count += 1
        return fields, data_  # list and list of lists

    def conversion_checks_writing(self, data_, fields_):
        """
        Loops through list of lists and converts to Row class objects
        :param data_:
        :return:
        """
        count = 1
        single_json_obj, array_type_member = {}, []
        invalid_rows, invalid_row_states = [], []
        for i in data_:
            record = Row(fields_, i, count)
            record.fields_data_len_check()
            state_id = record.id_check()
            state_type = record.type_check()
            state_type_desc = record.type_desc_check()
            state_e_or_n = record.E_or_N_checks()
            state_location = record.location_checks()
            state_cell = record.cell_checks()
            state_signal_group = record.signal_group_checks()
            state_asset_status = record.asset_status_check()
            state_install_engineer_check = record.install_engineer_check()
            state_install_date = record.install_date_check()
            states = [state_id, state_type, state_type_desc, state_e_or_n, state_location,
                      state_cell, state_signal_group, state_asset_status, state_install_engineer_check,
                      state_install_date]
            # if record validity == TRUE for all checks:
            if all(state is True for state in states):
                # print('save this record', record.row_id)
                valid_row = ValidRow(record.fields, record.row, record.row_id)
                inner_json_obj = valid_row.convert_to_json()
                array_type_member.append(inner_json_obj)
            else:
                # print('issue with', record.row_id)
                invalid_row = InvalidRow(record.fields, record.row, record.row_id)
                invalid_rows.append(invalid_row)
                invalid_row_states.append(states)
            count += 1

        single_json_obj['records'] = array_type_member

        print(single_json_obj)

        valid_row.write_to_json(single_json_obj)
        invalid_row.write_to_csv(invalid_rows, invalid_row_states)
        return


# ---- General Functions

    def is_integer(self,n):
        """
        Returns a boolean whether n is an integer or not
        :param n:
        :return:
        """
        passed = False  # not passed, unless proven wrong
        try:
            if float(n).is_integer():
                passed = True
        except (ValueError, TypeError):
            pass
        else:
            raise (ValueError, TypeError)
        finally:
            if passed:
                return True
            else:
                return False

    def is_null(self, obj, row_id_):
        """
        confirms if an cell is empty
        :param obj: record location
        :param row_id_: row number
        :return: boolean
        """
        try:
            if obj and len(obj) > 0:  # len('') = 0
                # print(obj, 'Has a non-zero len and real val')
                return False
            else:
                raise ValueError
                return True
        except (ValueError, AssertionError) as err_2:
            # print(err_2, 'value in row ', row_id_, 'is null or zero length')
            return True
        else:
            print('some edge case in', row_id_, ' where try nor except ended is_null()')
            return True

    def longer_than(self, obj, n_char, row_id_):
        """
        confirm if obj is longer than n_char
        :param obj: data record
        :param n_char: user defined
        :param row_id_: row number
        :return: Boolean. True if n_char longer than len(obj)
        """
        try:
            if len(obj) > n_char:
                # print(obj, "longer than ",n_char," permitted chars, in record row: ", row_id_)
                return True
            else:
                return False
        except TypeError:
            return False
        else:
            print('some edge case in', row_id_, ' where try nor except ended longer_than()')
            return False

    def val_lies_between(self, val, min, max, row_id_):
        """
        Function to confirm if a value lies betweena  min, max
        :param val: value to check (numeric)
        :param min: minimum numeric bound (numeric)
        :param max: maximum numeric bound (numeric)
        :param row_id_: row number
        :return: Boolean
        """

        if ConversionModule().longer_than(val, n_coord_ref, row_id_):
            return False
        val = int(val)
        try:
            if min <= val <= max:
                # print('does lie within')
                return True
            else:
                print('Row ', row_id_, "'s value", val, " not within range", min,
                      max)  # doesn't print as being caught by the Try Except
                return False
        except ValueError:
            pass
        else:
            print('some edge case in', row_id_, ' where try nor except ended val_lies_between()')
            return False

    def val_present_in(self, val, obj):
        """
        check if val is not in obj (lists)
        :param val: search val
        :param obj: obj to search (list)
        :return: Boolean: True if  present
        """
        if not ConversionModule().is_string(val):  # covers False + Null
            print('non-string value')
            return False

        if val in obj:
            # print(val, ' is within :', obj)
            return True
        else:
            # print(val, 'not within type:', obj)
            return False

    def is_string(self, string):
        """
        function to check if object is a string
        :param string: a suspected string object
        :return: boolean confirming if object is a string
        """
        try:
            if isinstance(string, str):
                return True
        except TypeError:
            pass
        else:
            print('try not except in is_string() was activated')
            return False


    def split_str_on(self, string, char):
        """
        function to split a string on a chosen character
        :param string: string to split
        :param char: character of your choice
        :return: list depending on n split-chars present
        """
        try:
            return string.split(char)
        except ValueError:
            print('string ', string, ' not splittable on', char, '. Check if split char is present or if string is null')
            return string


    def int_check_each_letter_in_each_word(self, list_of_words):
        """
        Function to loop over every letter in each word and check if each char is an integer
        :param list_of_words:
        :return: boolean
        """
        for word in list_of_words:
            for char in word:
                if ConversionModule().is_integer(char) is not True:  # covers False + Null
                    print("Character ", char, " in ", word, " is not an int. Check format")
                    return False  # if not int, end id_check
        return True


    def if_null_return_empty_string(self, string):
        """
        checks a string to see if longer than 0 chars
        :param string: string to len check
        :return: if longer than 0, returns input string, else returns ""
        """
        if ConversionModule().longer_than(str(string), 0, None):
            return str(string)
        else:
            return ""




    def quality_check(self, fields_, data_, set_n_fields=0):
        """
        checks the number of fields
        :param fields_: list of fields,
        :param data_: list of lists of each row
        :param set_n_fields: entered by the user if different from default of 'len(fields)'. Dummy numeric var '0'
        :return: nothing. raise a TypeError if len(fields) != len(columns in row)
        """
        if set_n_fields == 0:
            n_cols_ = len(fields_)
        else:
            n_cols_ = set_n_fields
            ConversionModule().is_integer(n_cols_)
        # print('n fields is ', n_cols_)

        # should be len(fields_) even if filled with Nulls, but just remove any unexpected cases
        for row in data_:
            if len(row) < len(fields_):
                print('row length shorter than n fields', row)
                raise TypeError
        return

# -----


class Row(ConversionModule):
    def __init__(self, fields_, row, row_id):
        """
        Overarching Row Class
        :param fields_: takes headers of file
        :param row: the row's data [val1, val2, ...]
        :param row_id: an arbitrary row number assigned during a first loop. For quick finding by human
        """
        self.row = row  # actual to do len checks
        self.row_id = row_id
        self.fields = fields_
        self.id = row[0]
        self.rec_type = row[1]
        self.typeDesc = row[2]
        self.installDate = row[3]
        self.easting = row[4]
        self.northing = row[5]
        self.location = row[6]
        self.controlServer = row[7]
        self.signalGroup = row[8]
        self.status = row[9]
        self.installedBy = row[10]

    def fields_data_len_check(self):
        """
        Function to just check if the n header cols matchers n cols of data
        CURRENTLY NOT WORKING AS EXPECTED
        :return: nothing, raises error if lengths don't match
        """
        if len(self.row) != len(self.fields):
            raise ValueError(
                "The n fields in the input file does not match the the data. Check if you are missing a header")
        else:
            # print('Row', self.row_id, ' good')
            pass

    def id_check(self):
        """
        function to check if the id value is correctly formatted
        checks for: is_null(), splittable on char, if chars are integers
        :return: boolean
        """
        if ConversionModule().is_null(self.id, self.row_id):
            return False  # if true end the func (stop iteration in loop)

        id_parts = ConversionModule().split_str_on(self.id, '/')
        # print('split is: ',id_parts, len(id_parts))
        try:
            if len(self.id) != id_len:
                raise ValueError("ID ", self.id, " in row", self.row_id, " not ", id_len,
                                 " characters long. Check ID format")
                return False
            if len(id_parts) != n_id_parts:
                raise ValueError("ID ", self.id, " not splittable into two parts on '/'. Check ID format")
                return False
        except(ValueError) as err_3:
            print(err_3, 'in this bit log the record as an invalid row', self.row_id)
            return False  # end id_check & carry on

        # loop over each char and chek if int
        int_check = ConversionModule().int_check_each_letter_in_each_word(id_parts)
        if int_check:
            return True
        else:
            return False

    def type_check(self):
        """
        undertakes type checks of, is_null, is in permitted 'asset_type_codes'
        :return: boolean
        """
        # check no null constraint, log within func
        if ConversionModule().is_null(self.rec_type, self.row_id):
            print('type is null')  # rm later
            return False  # end the func (stop iteration in loop)

        else:
            # check for permitted asset_type_codes
            if ConversionModule().val_present_in(self.rec_type, asset_type_codes):
                # print('val', self.rec_type,'present in ', asset_type_codes)
                return True
            else:
                print('row:', self.row_id, "'s value", self.rec_type, 'not in', asset_type_codes)
                return False

    def type_desc_check(self):
        """
        undertakes type checks of, is_null, if is less than len(type_desc_length) chars
        :return: boolean
        """
        # check no null constraint, log within func
        if ConversionModule().is_null(self.typeDesc, self.row_id):
            print('type_desc_check() was null')
            return False  # end the func (stop iteration in loop)
        # check length < 11 char
        elif ConversionModule().longer_than(self.typeDesc, type_desc_length, self.row_id):
            # print('type_desc_check() longer than 11')
            return False  # end
        else:
            # print('passes all tests')
            return True

    def install_date_check(self):
        """
        checks to ensure valid date format of dd-MM-yyyy or is null
        is null, is it separable on '-' into 3 parts, are expected characters integers, are expected months in 12 months
        :return: boolean
        """
        # if pass the 'is null' test, succeed validity tests and end checks
        if ConversionModule().is_null(self.installDate, self.row_id):
            return True

        date_parts = ConversionModule().split_str_on(self.installDate, '-')
        try:
            # if not 3 parts, fail validity check
            if len(date_parts) != len(len_date_parts):
                print('date not 3 parts')
                raise ValueError("installDate ", self.installDate, " in row", self.row_id, " not ", len(len_date_parts),
                                 " characters long. Check dateFormat")
                return False
            # check the lengths of each dd-MMM-yyyy match up. if not fail valid test
            if len(date_parts[0]) != len_date_parts[0] \
                    or len(date_parts[1]) != len_date_parts[1] \
                    or len(date_parts[2]) != len_date_parts[2]:
                print('some parts too short ')
                raise ValueError("Date ", self.installDate, " not all parts are correct lengths of ", len_date_parts,
                                 " Check Date  format")
                # stop code/log is problematic and carry on
                return False
            # if fail month check, fail the validity test
            if ConversionModule().val_present_in(date_parts[1], months) is False:
                print('failed month check')
                return False
            # if fails each car an int test, fail the validity test
            if ConversionModule().int_check_each_letter_in_each_word([date_parts[0], date_parts[2]]) is False:
                print('test ran')
                return False
            # would also like to put in a check if date is not in the future, I see year '2096'. But this would require
            # use of date, time modules
            # print(self.installDate,'passed all date checks')
            return True  # end date_checks
        except(ValueError) as err_4:
            print(err_4, 'in this bit log the record as an invalid row', self.row_id)
            # ensure to log this row number as invalid
            return False  # end date_check
        else:
            print('catchalll where try or except did not catch all install_dat_check() outcomes')
            return False

    def E_or_N_checks(self):
        """
        checks if in allowed coordinates, dictated by MinBoundingRecangle
        :return: boolean
        """
        # coords must be non-null
        if ConversionModule().is_null(self.easting, self.row_id) \
                or ConversionModule().is_null(self.northing, self.row_id):
            return False  # end the func (stop iteration in loop)
        # is coords aren't an int, return fail valid check
        if ConversionModule().is_integer(self.easting) is False or ConversionModule().is_integer(self.northing) is False:
            return False
        # fail valid check if coords not between min-max
        if ConversionModule().val_lies_between(self.easting, mbr[0], mbr[1], self.row_id) is False or \
                ConversionModule().val_lies_between(self.northing, mbr[2], mbr[3], self.row_id) is False:
            return False
        else:
            # print('succeeds E_or_N_chekcs()')
            return True

    def location_checks(self):
        """
        checks to see if a record's location is not too long. controlled by 'location_length
        :return: boolean, stops if too long
        """
        if ConversionModule().longer_than(self.location, location_length, self.row_id):
            return False
        else:
            return True

    def cell_checks(self):
        """
        checks Asset Control Server's type is in permitted 'asset_control_servers'
        :return: boolean
        """
        # if null is fine - no null check
        try:
            if ConversionModule().val_present_in(self.controlServer, asset_control_servers):
                return True
            else:
                print(self.controlServer, ' not in ', asset_control_servers)
                return False
        except ValueError:
            print('cell check failed')
            pass
        else:
            print('edgecase where cell_check() not ended by try or except')
            return False

    def signal_group_checks(self):
        """
        checks Signal group to ensure it is no longer than 'sig_gr_char_len' characters
        :return: boolean
        """
        try:
            if ConversionModule().is_null(self.signalGroup, self.row_id):  # if not given, ok
                return True
            elif ConversionModule().longer_than(self.signalGroup, sig_gr_char_len,
                             self.row_id) is False:  # otherwise must be shorter than 5
                # print('signal_group_checks() not longer than 11')
                return True
            else:
                print('some catchall')
                return False
        except ValueError:
            print('signal_group_checks failed')
            pass
        else:
            print('edgecase where signal_group_checks() not ended by try or except')
            return False

    def asset_status_check(self):
        """
        checks to see if Asset Status is within asset_statuses (list) object. 'Active' or 'Proposed'
        :return: boolean if status within permitted 'asset_statuses'
        """
        try:
            if ConversionModule().is_null(self.status, self.row_id):
                return False
            elif ConversionModule().val_present_in(self.status, asset_statuses):
                # print('success')
                return True
            else:
                print('issue with', self.row_id, ': ', self.status, 'not within', asset_statuses)
                return False
        except (TypeError, ValueError):
            pass
        else:
            print('edgecase where asset_status_check() not ended by try or except')
            return False

    def install_engineer_check(self):
        """
        checks to ensure that value is either Null or not longer than 'engineer_char_length' characters
        :return:
        """
        try:
            if ConversionModule().is_null(self.installedBy, self.row_id):  # if null, finish checks - ok
                # print('null is ok')
                return True
            elif ConversionModule().longer_than(self.installedBy, engineer_char_length, self.row_id):
                # print(self.installedBy, 'is longer than', engineer_char_length)
                return False
            else:
                # if less than 15
                # print(self.installedBy, 'is less than', engineer_char_length)
                return True
        except (TypeError, ValueError):
            print('err encountered')
            return False
        else:
            print('edgecase where install_engineer_check() not ended by try or except')
            return False


class ValidRow(Row):
    """
    Child class of Row(). Using all the same self attributes, but specific methods on writing
    """
    pass

    def convert_to_json(self):
        """
        convert each field value into Required Value Conversion from CSV to JSON
        :return: a single json record with all 'fields' as strings in the required format
        """
        json_record = {}
        json_record['id'] = str(self.id)
        json_record['type'] = str(self.rec_type)
        json_record['typeDescription'] = str(self.typeDesc)
        json_record['installationDate'] = str(ConversionModule().if_null_return_empty_string(self.installDate))
        if json_record['installationDate'] != "":  # if empty string, do not execute rearrange (below)
            date_parts_ = ConversionModule().split_str_on(self.installDate, '-')
            date_parts_[1] = month_text_to_numeric[date_parts_[1]]  # convert 'DEC' to '12'
            json_record['installationDate'] = str(
                date_parts_[2] + '-' + date_parts_[1] + '-' + date_parts_[0])  # dd-MM-yyyy --> yyyy-mm-dd
        json_record['easting'] = int(self.easting)
        json_record['northing'] = int(self.northing)
        json_record['location'] = str(ConversionModule().if_null_return_empty_string(self.location))
        json_record['controlServer'] = str(ConversionModule().if_null_return_empty_string(self.controlServer))
        json_record['signalGroup'] = str(ConversionModule().if_null_return_empty_string(self.signalGroup))
        json_record['status'] = str(self.status)
        json_record['installedBy'] = str(ConversionModule().if_null_return_empty_string(self.installedBy))

        return json_record

    def write_to_json(self, json_object):
        """
        writes a nested dictionary to a json file
        :param json_object: a json object containing all valid rows of data
        :return: None
        """
        with open('Sample Data.json', 'w') as my_json_file:
            my_json_file.write(str(json_object))
        return


class InvalidRow(Row):
    """
    Child class of Row(). Using all the same self attributes, but specific methods on writing
    """
    pass

    def write_to_csv(self, rows, row_states):
        """
        funciton to write the invalid rows to a csv file. Identifies which test(s) the record failed on, and
        also its row number and unique ID. Includes row number in case unique ID fails to be unique
        :param rows: a list containing each InvalidRow
        :param row_states: a list of 'states' (validity check outcomes) for each row [T, F, ...]
        :return:
        """
        with open('Sample Data Invalid.csv', 'w') as file:
            new_fields = self.fields
            new_fields.append('Row_Id')
            new_fields.append('ID')
            for i in new_fields:
                file.write(str(i) + ',')
            file.write('\n')
            # now write the states
            for row in range(len(row_states)):
                for state in row_states[row]:  # for each True, False for each row
                    file.write(str(state) + ',')
                file.write(str(rows[row].row_id) + ',' + str(rows[row].id) + ',' + '\n')
        return




def main():
    """  File to convert .csv data to .json data only if a series of validity checks are passed.
    full details are available in;
     'Developer (GIS) Python Programming Exercise - 4303817.pdf' and
     'Data Documentation and Mappings.pdf'
    :return: 1) files converted to json   2) invalid file list as csv
    """
    print('Hello TfL')
    print(main.__doc__)

    fields, data = ConversionModule().read_csv(file_name)
    ConversionModule().quality_check(fields, data)  # test: set_n_fields=4, 4.2
    ConversionModule().conversion_checks_writing(data, fields)

    # After thoughts:
    # Have moved to everything within classes, but unclear on the benefit over previous 'imperative-with-OOP-methods'


if __name__ == '__main__':  # main.py
    main()
