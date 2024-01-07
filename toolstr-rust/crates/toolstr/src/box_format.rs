use crate::FormatError;
use toolstr_colored::{Color, Colorize};

/// Theme
#[derive(Clone)]
pub struct Theme {
    /// border chars
    pub border_chars: BorderChars,
    /// border style
    pub border_style: FontStyle,
    /// title style
    pub title_style: FontStyle,
}

impl Default for Theme {
    fn default() -> Theme {
        Theme {
            border_chars: BorderChars::default(),
            border_style: FontStyle::default(),
            title_style: FontStyle("".bold()),
        }
    }
}

impl Theme {
    /// set border chars
    pub fn with_border_chars(mut self, border_chars: BorderChars) -> Theme {
        self.border_chars = border_chars;
        self
    }

    /// set border style
    pub fn with_border_style(mut self, border_style: FontStyle) -> Theme {
        self.border_style = border_style;
        self
    }

    /// set title style
    pub fn with_title_style(mut self, title_style: FontStyle) -> Theme {
        self.title_style = title_style;
        self
    }
}

/// border chars
#[derive(Clone)]
pub struct BorderChars {
    /// vertical border
    pub vertical: String,
    /// horizontal border
    pub horizontal: String,
    /// top left border
    pub top_left: String,
    /// top right border
    pub top_right: String,
    /// bottom left border
    pub bottom_left: String,
    /// bottom right border
    pub bottom_right: String,
    /// cross border
    pub cross: String,
    /// top cross border
    pub top_cross: String,
    /// bottom_cross border
    pub bottom_cross: String,
    /// left cross border
    pub left_cross: String,
    /// right cross border
    pub right_cross: String,
}

impl Default for BorderChars {
    fn default() -> BorderChars {
        BorderChars {
            vertical: "│".to_string(),
            horizontal: "─".to_string(),
            top_left: "┌".to_string(),
            top_right: "┐".to_string(),
            bottom_left: "└".to_string(),
            bottom_right: "┘".to_string(),
            cross: "┼".to_string(),
            top_cross: "┬".to_string(),
            bottom_cross: "┴".to_string(),
            left_cross: "├".to_string(),
            right_cross: "┤".to_string(),
        }
    }
}

/// font style
#[derive(Default, Clone, Debug)]
pub struct FontStyle(pub toolstr_colored::ColoredString);

impl From<toolstr_colored::ColoredString> for FontStyle {
    fn from(value: toolstr_colored::ColoredString) -> FontStyle {
        FontStyle(value)
    }
}

impl From<toolstr_colored::Color> for FontStyle {
    fn from(value: toolstr_colored::Color) -> FontStyle {
        FontStyle("".color(value))
    }
}

impl FontStyle {
    /// format string using style
    pub fn format<T: AsRef<str>>(&self, text: T) -> String {
        let FontStyle(style) = self;
        let mut s = style.clone();
        s.input = text.as_ref().to_string();
        s.to_string()
    }

    /// format string using style
    pub fn println<T: AsRef<str>>(&self, text: T) {
        println!("{}", self.format(text))
    }

    /// make style bold
    pub fn bold(&mut self) {
        self.0 = self.0.clone().bold();
    }
}

/// convert a test string to a Color
pub fn hex_to_color(hex: &str) -> Result<Color, FormatError> {
    // Remove '#' if it exists
    let hex = hex.strip_prefix('#').unwrap_or(hex);

    // Check if the string is of the correct length
    if hex.len() != 6 {
        return Err(FormatError::InvalidFormat(
            "Invalid length for a hex color string".to_string(),
        ));
    }

    // Parse each color component
    let r = u8::from_str_radix(&hex[0..2], 16)
        .map_err(|_| FormatError::InvalidFormat("Invalid hex value for red".to_string()))?;
    let g = u8::from_str_radix(&hex[2..4], 16)
        .map_err(|_| FormatError::InvalidFormat("Invalid hex value for green".to_string()))?;
    let b = u8::from_str_radix(&hex[4..6], 16)
        .map_err(|_| FormatError::InvalidFormat("Invalid hex value for blue".to_string()))?;

    Ok(Color::TrueColor { r, g, b })
}

/// convert to title style
pub trait ToTheme {
    /// convert to title style
    fn to_theme(&self) -> Theme;
}

impl<T: ToTheme> ToTheme for Option<T> {
    fn to_theme(&self) -> Theme {
        match self {
            Some(value) => value.to_theme(),
            None => Theme::default(),
        }
    }
}

impl<T: ToTheme> ToTheme for &Option<T> {
    fn to_theme(&self) -> Theme {
        match self {
            Some(value) => value.to_theme(),
            None => Theme::default(),
        }
    }
}

impl ToTheme for Theme {
    fn to_theme(&self) -> Theme {
        self.clone()
    }
}

impl ToTheme for &Theme {
    fn to_theme(&self) -> Theme {
        (*self).clone()
    }
}

/// print text box
pub fn print_text_box<A: AsRef<str>, T: ToTheme>(text: A, style: T) {
    let text = text.as_ref();
    let theme = style.to_theme();
    let top = format!(
        "{}{}{}",
        theme.border_chars.top_left,
        theme.border_chars.horizontal.repeat(text.len() + 2),
        theme.border_chars.top_right
    );
    theme.border_style.println(top);
    println!(
        "{} {} {}",
        theme.border_style.format(&theme.border_chars.vertical),
        theme.title_style.format(text),
        theme.border_style.format(&theme.border_chars.vertical),
    );
    let bottom = format!(
        "{}{}{}",
        theme.border_chars.bottom_left,
        theme.border_chars.horizontal.repeat(text.len() + 2),
        theme.border_chars.bottom_right
    );
    theme.border_style.println(bottom);
}

/// print header
pub fn print_header<A: AsRef<str>, T: ToTheme>(text: A, style: T) {
    let text = text.as_ref();
    let theme = style.to_theme();
    let underline = theme.border_chars.horizontal.repeat(text.len());
    theme.title_style.println(text);
    theme.border_style.println(underline);
}
