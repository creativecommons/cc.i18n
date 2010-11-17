import os
import tempfile

from cc.i18n import util


def test_get_all_trans_stats():
    """
    Test the get_all_trans_stats utility function.
    """
    temp_dir = tempfile.mkdtemp()

    # write a fake CSV file
    transstats = os.path.join(temp_dir, 'transstats.csv')
    ts_file = file(transstats, 'w')
    ts_file.write(
        ('es_AR,564,343,27,60\n'
         'en_US,564,0,1,0\n'
         'hr,564,447,17,79\n'
         'no,564,400,14,70'))
    ts_file.close()

    expected = {
        'es_AR': {
            'num_messages': 564,
            'num_trans': 343,
            'num_fuzzy': 27,
            'num_untrans': 194,
            'percent_trans': 60},
        'en_US': {
            'num_messages': 564,
            'num_trans': 0,
            'num_fuzzy': 1,
            'num_untrans': 563,
            'percent_trans': 0},
        'hr': {
            'num_messages': 564,
            'num_trans': 447,
            'num_fuzzy': 17,
            'num_untrans': 100,
            'percent_trans': 79},
        'no': {
            'num_messages': 564,
            'num_trans': 400,
            'num_fuzzy': 14,
            'num_untrans': 150,
            'percent_trans': 70}}

    results = util.get_all_trans_stats(transstats)
    assert results == expected

    # overwrite that old CSV file,
    ts_file = file(transstats, 'w')
    ts_file.write(
        ('es_AR,999,999,999,999\n'
         'en_US,999,999,999,999\n'
         'hr,999,999,999,999\n'
         'no,999,999,999,999'))
    ts_file.close()

    # make sure it cached the old results
    results = util.get_all_trans_stats(transstats)
    assert results == expected


def test_get_well_translated_langs():
    """
    Test the util.get_well_translated_langs function.
    """
    temp_dir = tempfile.mkdtemp()

    # write a fake CSV file
    transstats = os.path.join(temp_dir, 'transstats.csv')
    ts_file = file(transstats, 'w')
    ts_file.write(
        ('es_AR,564,343,27,60\n'
         'en,564,0,0,0\n'
         'en_US,564,0,1,0\n'
         'hr,564,447,17,79\n'
         'no,564,400,14,70\n'
         'nl,564,456,16,80\n'
         'fi,564,460,14,81'))
    ts_file.close()

    expected_zero = [
        {'code': 'es_AR', 'name': u'Castellano (AR)'},
        {'code': 'en', 'name': u'English'},
        {'code': 'en_US', 'name': u'English (US)'},
        {'code': 'hr', 'name': u'hrvatski'},
        {'code': 'nl', 'name': u'Nederlands'},
        {'code': 'no', 'name': u'Norsk'},
        {'code': 'fi', 'name': u'Suomeksi'}]
    assert util.get_well_translated_langs(0, transstats) == expected_zero

    expected_seventy = [
        {'code': 'en', 'name': u'English'},
        {'code': 'hr', 'name': u'hrvatski'},
        {'code': 'nl', 'name': u'Nederlands'},
        {'code': 'no', 'name': u'Norsk'},
        {'code': 'fi', 'name': u'Suomeksi'}]
    assert util.get_well_translated_langs(70, transstats) == expected_seventy

    expected_eighty = [
        {'code': 'en', 'name': u'English'},
        {'code': 'nl', 'name': u'Nederlands'},
        {'code': 'fi', 'name': u'Suomeksi'}]
    assert util.get_well_translated_langs(80, transstats) == expected_eighty

    # Test caching: overwrite the old file with bogus data, we should
    # get the old results
    ts_file = file(transstats, 'w')
    ts_file.write(
        ('es_AR,999,999,999,999\n'
         'en,999,999,999,999\n'
         'en_US,999,999,999,999\n'
         'hr,999,999,999,999\n'
         'no,999,999,999,999\n'
         'nl,999,999,999,999\n'
         'fi,999,999,999,999'))
    ts_file.close()
    assert util.get_well_translated_langs(80, transstats) == expected_eighty

    # English shouldn't show up if we tell it not to
    expected_eighty_noenglish = [
        {'code': 'nl', 'name': u'Nederlands'},
        {'code': 'fi', 'name': u'Suomeksi'}]
    assert util.get_well_translated_langs(
        80, transstats, False) == expected_eighty_noenglish