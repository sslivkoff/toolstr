use unicode_truncate::{Alignment, UnicodeTruncateStr};

/// line count of String or &str
pub fn n_lines<T: AsRef<str>>(s: T) -> usize {
    s.as_ref().chars().filter(|&c| c == '\n').count()
}

/// width of String or &str
pub fn width<T: AsRef<str>>(s: T) -> usize {
    s.as_ref()
        .split('\n')
        .map(|s| s.chars().count())
        .max()
        .unwrap_or(0)
    // .map(unicode_width::UnicodeWidthStr::width)
    // .map(unicode_width::UnicodeWidthStr::width_cjk)
}

/// width of a single line
pub fn line_width<T: AsRef<str>>(s: T) -> usize {
    s.as_ref().chars().count()
}

/// lines of String or &str
pub fn lines<T: AsRef<str>>(s: T) -> Vec<String> {
    s.as_ref().split('\n').map(|s| s.to_string()).collect()
}

/// multiline align left
pub fn align_left<T: AsRef<str>>(s: T, width: usize) -> String {
    s.as_ref()
        .split('\n')
        .map(|s| align_line_left(s, width))
        .collect::<Vec<_>>()
        .join("\n")
}

/// multiline align right
pub fn align_right<T: AsRef<str>>(s: T, width: usize) -> String {
    s.as_ref()
        .split('\n')
        .map(|s| align_line_right(s, width))
        .collect::<Vec<_>>()
        .join("\n")
}

/// align single line left
pub fn align_line_left<T: AsRef<str>>(s: T, width: usize) -> String {
    s.as_ref().unicode_pad(width, Alignment::Left, false).into()
}

/// align single line right
pub fn align_line_right<T: AsRef<str>>(s: T, width: usize) -> String {
    s.as_ref()
        .unicode_pad(width, Alignment::Right, false)
        .into()
}
