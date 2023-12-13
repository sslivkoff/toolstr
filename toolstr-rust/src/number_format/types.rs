#[cfg(test)]
#[path = "types_tests.rs"]
mod tests;

use crate::FormatError;

pub(crate) const PREFIXES: [&str; 17] = [
    "y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y",
];

pub(crate) const DECIMAL_CHAR: char = '.';
pub(crate) const GROUP_DELIMITER_CHAR: char = ',';

// default number format settings
pub(crate) const DEFAULT_ZERO_PADDING: bool = true;
pub(crate) const DEFAULT_FILL: char = ' ';
pub(crate) const DEFAULT_ALIGN: NumberAlign = NumberAlign::Right;
pub(crate) const DEFAULT_SIGN: Sign = Sign::OnlyNegative;
pub(crate) const DEFAULT_TYPE_PREFIX: bool = false;
pub(crate) const DEFAULT_MIN_WIDTH: usize = 0;
pub(crate) const DEFAULT_MAX_WIDTH: usize = usize::MAX;
pub(crate) const DEFAULT_COMMAS: bool = false;
pub(crate) const DEFAULT_PRECISION: usize = 6;
pub(crate) const DEFAULT_FORMAT_TYPE: FormatType = FormatType::None;
pub(crate) const DEFAULT_TIMEZONE: Timezone = Timezone::Utc;

/// Represents a destructured specification of a provided format pattern string.
#[derive(Debug, Clone)]
pub struct NumberFormat {
    /// zero padding
    pub zero_padding: bool,
    /// fill character
    pub fill: char,
    /// alignment
    pub align: NumberAlign,
    /// sign
    pub sign: Sign,
    /// type prefix
    pub type_prefix: bool,
    /// min_width
    pub min_width: usize,
    /// max_width
    pub max_width: usize,
    /// commas
    pub commas: bool,
    /// decimals
    pub precision: usize,
    /// format type
    pub format_type: FormatType,
    /// timezone
    pub timezone: Timezone,
}

#[derive(Debug, Clone)]
pub enum Timezone {
    Local,
    Utc,
}

impl NumberFormat {
    /// format number value
    pub fn format<T: Into<f64>>(&self, input: T) -> Result<String, FormatError> {
        let s = super::interface::number_format(self, input)?;
        if s.len() < self.min_width {
            match self.align {
                NumberAlign::Left => Ok(format!("{:<width$}", s, width = self.min_width)),
                NumberAlign::Right => Ok(format!("{:>width$}", s, width = self.min_width)),
                _ => todo!("center align"),
            }
        } else if s.len() > self.max_width {
            if self.max_width == 1 {
                Ok(".".to_string())
            } else if self.max_width == 2 {
                Ok("..".to_string())
            } else {
                Ok(format!("{}...", &s[0..(self.max_width - 3)]))
            }
        } else {
            Ok(s)
        }
    }

    /// format option of binary data
    pub fn format_option<T: Into<f64>, S: AsRef<str>>(
        &self,
        input: Option<T>,
        none_str: S,
    ) -> Result<String, FormatError> {
        match input {
            Some(data) => self.format(data),
            None => Ok(none_str.as_ref().to_string()),
        }
    }
}

impl Default for NumberFormat {
    fn default() -> NumberFormat {
        NumberFormat {
            zero_padding: DEFAULT_ZERO_PADDING,
            fill: DEFAULT_FILL,
            align: NumberAlign::default(),
            sign: Sign::default(),
            type_prefix: DEFAULT_TYPE_PREFIX,
            min_width: DEFAULT_MIN_WIDTH,
            max_width: DEFAULT_MAX_WIDTH,
            commas: DEFAULT_COMMAS,
            precision: DEFAULT_PRECISION,
            format_type: FormatType::default(),
            timezone: DEFAULT_TIMEZONE,
        }
    }
}

/// NumberAlignment
#[derive(Debug, PartialEq, Eq, Clone)]
pub enum NumberAlign {
    /// left align
    Left,
    /// right align
    Right,
    /// center align
    Center,
    /// center align with sign on left side
    SignedRight,
}

impl Default for NumberAlign {
    fn default() -> NumberAlign {
        DEFAULT_ALIGN
    }
}

/// Whether to include sign
#[derive(Debug, PartialEq, Eq, Clone)]
pub enum Sign {
    /// only show sign when negative
    OnlyNegative,
    /// always show sign
    Always,
    /// space or dash
    SpaceOrDash,
}

impl Default for Sign {
    fn default() -> Sign {
        DEFAULT_SIGN
    }
}

/// format type
#[derive(Debug, PartialEq, Eq, Clone)]
pub enum FormatType {
    /// exponent format
    Exponent,
    /// exponent upper case format
    ExponentUppercase,
    /// fixed point format
    FixedPoint,
    /// SI prefix format
    SI,
    /// percentage format
    Percentage,
    /// binary format
    Binary,
    /// octal format
    Octal,
    /// octal upper case format
    OctalUppercase,
    /// decimal format
    Decimal,
    /// hex format
    Hex,
    /// hex upper case format
    HexUppercase,
    /// integer order of magnitude (display integer when <1000)
    IntegerOrderOfMagnitude,
    /// float order of magnitude (display as float when <1000)
    FloatOrderOfMagnitude,
    /// timestamp pretty
    TimestampPretty,
    /// no format
    None,
}

impl FormatType {
    /// list all FormatType variants
    pub fn all_variants() -> Vec<FormatType> {
        vec![
            FormatType::Exponent,
            FormatType::ExponentUppercase,
            FormatType::FixedPoint,
            FormatType::SI,
            FormatType::Percentage,
            FormatType::Binary,
            FormatType::Octal,
            FormatType::OctalUppercase,
            FormatType::Decimal,
            FormatType::Hex,
            FormatType::HexUppercase,
            FormatType::IntegerOrderOfMagnitude,
            FormatType::FloatOrderOfMagnitude,
            FormatType::TimestampPretty,
            FormatType::None,
        ]
    }
}

impl Default for FormatType {
    fn default() -> FormatType {
        DEFAULT_FORMAT_TYPE
    }
}
