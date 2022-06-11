import nciraspw.files


def test_all_files_exist() -> None:
    for ras_pw_file in nciraspw.files.RasPathwayDataFile:
        assert nciraspw.files.ras_pw_file_exists(ras_pw_file)
