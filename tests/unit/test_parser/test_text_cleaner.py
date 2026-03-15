from resume2job.parser.text_cleaner import clean_text


class TestCleanText:
    def test_whitespace_collapsing(self) -> None:
        result = clean_text("hello    world")
        assert result == "hello world"

    def test_tabs_collapsed(self) -> None:
        result = clean_text("hello\t\tworld")
        assert result == "hello world"

    def test_newline_normalization(self) -> None:
        result = clean_text("hello\n\n\n\nworld")
        assert result == "hello\n\nworld"

    def test_two_newlines_preserved(self) -> None:
        result = clean_text("hello\n\nworld")
        assert result == "hello\n\nworld"

    def test_bullet_normalization_bullet(self) -> None:
        result = clean_text("• item one")
        assert result == "- item one"

    def test_bullet_normalization_square(self) -> None:
        result = clean_text("▪ item two")
        assert result == "- item two"

    def test_bullet_normalization_filled_circle(self) -> None:
        result = clean_text("● item three")
        assert result == "- item three"

    def test_control_character_stripping(self) -> None:
        text = "hello\x00world\x01test"
        result = clean_text(text)
        assert "\x00" not in result
        assert "\x01" not in result
        assert "hello" in result
        assert "world" in result

    def test_page_number_removal(self) -> None:
        result = clean_text("Some text\nPage 1 of 3\nMore text")
        assert "Page 1 of 3" not in result
        assert "page 1 of 3" not in result
        assert "Some text" in result
        assert "More text" in result

    def test_page_number_case_insensitive(self) -> None:
        result = clean_text("page 2 of 5")
        assert result == ""

    def test_empty_input(self) -> None:
        assert clean_text("") == ""

    def test_none_input(self) -> None:
        assert clean_text(None) == ""

    def test_unicode_nfkd_normalization(self) -> None:
        # fi ligature (U+FB01) should be normalized to "fi"
        result = clean_text("\ufb01nance")
        assert "fi" in result

    def test_strips_leading_trailing_whitespace(self) -> None:
        result = clean_text("  hello world  ")
        assert result == "hello world"

    def test_line_stripping(self) -> None:
        result = clean_text("  line one  \n  line two  ")
        assert result == "line one\nline two"
