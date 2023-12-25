use crate::{
    BinaryFormat, BoolFormat, FormatError, FormatType, NumberFormat, StringFormat, UnknownFormat,
};
use polars::prelude::DataType;

/// cell format shorthand
#[derive(Debug, Clone)]
pub enum DatumFormatShorthand {
    /// number format
    Number(NumberFormat),
    /// binary format
    Binary(BinaryFormat),
    /// string format
    String(StringFormat),
    /// bool format
    Bool(BoolFormat),
    /// unknown format
    Unknown(UnknownFormat),
}

impl From<NumberFormat> for DatumFormatShorthand {
    fn from(format: NumberFormat) -> DatumFormatShorthand {
        DatumFormatShorthand::Number(format)
    }
}

impl From<StringFormat> for DatumFormatShorthand {
    fn from(format: StringFormat) -> DatumFormatShorthand {
        DatumFormatShorthand::String(format)
    }
}

impl From<BinaryFormat> for DatumFormatShorthand {
    fn from(format: BinaryFormat) -> DatumFormatShorthand {
        DatumFormatShorthand::Binary(format)
    }
}

impl From<BoolFormat> for DatumFormatShorthand {
    fn from(format: BoolFormat) -> DatumFormatShorthand {
        DatumFormatShorthand::Bool(format)
    }
}

impl DatumFormatShorthand {
    /// set min width
    pub fn min_width(self, min_width: usize) -> DatumFormatShorthand {
        match self {
            DatumFormatShorthand::Number(fmt) => {
                DatumFormatShorthand::Number(fmt.min_width(min_width))
            }
            DatumFormatShorthand::String(fmt) => {
                DatumFormatShorthand::String(fmt.min_width(min_width))
            }
            DatumFormatShorthand::Binary(fmt) => {
                DatumFormatShorthand::Binary(fmt.min_width(min_width))
            }
            DatumFormatShorthand::Bool(fmt) => DatumFormatShorthand::Bool(fmt.min_width(min_width)),
            DatumFormatShorthand::Unknown(fmt) => {
                DatumFormatShorthand::Unknown(fmt.min_width(min_width))
            }
        }
    }

    /// set max width
    pub fn max_width(self, max_width: usize) -> DatumFormatShorthand {
        match self {
            DatumFormatShorthand::Number(fmt) => {
                DatumFormatShorthand::Number(fmt.max_width(max_width))
            }
            DatumFormatShorthand::String(fmt) => {
                DatumFormatShorthand::String(fmt.max_width(max_width))
            }
            DatumFormatShorthand::Binary(fmt) => {
                DatumFormatShorthand::Binary(fmt.max_width(max_width))
            }
            DatumFormatShorthand::Bool(fmt) => DatumFormatShorthand::Bool(fmt.max_width(max_width)),
            DatumFormatShorthand::Unknown(fmt) => {
                DatumFormatShorthand::Unknown(fmt.max_width(max_width))
            }
        }
    }

    /// convert shorthand into formal version
    pub fn finalize(self, dtype: &DataType) -> Result<DatumFormat, FormatError> {
        let fmt = match self {
            DatumFormatShorthand::Number(fmt) => DatumFormat::Number(fmt),
            DatumFormatShorthand::Binary(fmt) => DatumFormat::Binary(fmt),
            DatumFormatShorthand::String(fmt) => DatumFormat::String(fmt),
            DatumFormatShorthand::Bool(fmt) => DatumFormat::Bool(fmt),
            DatumFormatShorthand::Unknown(fmt) => match dtype {
                DataType::Utf8 => DatumFormat::String(fmt.into()),
                DataType::Boolean => DatumFormat::Bool(fmt.into()),
                DataType::Binary => DatumFormat::Binary(fmt.into()),
                dtype if dtype.is_integer() => {
                    let fmt: NumberFormat = fmt.into();
                    let fmt = fmt.format_type(&FormatType::Decimal).precision(0);
                    DatumFormat::Number(fmt)
                }
                dtype if dtype.is_float() => {
                    let fmt: NumberFormat = fmt.into();
                    let fmt = fmt.format_type(&FormatType::Exponent);
                    DatumFormat::Number(fmt)
                }
                _ => {
                    return Err(FormatError::UnsupportedDatatype(format!(
                        "Unsupported datatype: {:?}",
                        dtype
                    )))
                }
            },
        };
        Ok(fmt)
    }
}

/// cell format
#[derive(Debug, Clone)]
pub enum DatumFormat {
    /// number format
    Number(NumberFormat),
    /// binary format
    Binary(BinaryFormat),
    /// string format
    String(StringFormat),
    /// bool format
    Bool(BoolFormat),
}

impl DatumFormat {
    /// set min width
    pub fn min_width(self, min_width: usize) -> DatumFormat {
        match self {
            DatumFormat::Number(fmt) => DatumFormat::Number(fmt.min_width(min_width)),
            DatumFormat::String(fmt) => DatumFormat::String(fmt.min_width(min_width)),
            DatumFormat::Binary(fmt) => DatumFormat::Binary(fmt.min_width(min_width)),
            DatumFormat::Bool(fmt) => DatumFormat::Bool(fmt.min_width(min_width)),
        }
    }

    /// set max width
    pub fn max_width(self, max_width: usize) -> DatumFormat {
        match self {
            DatumFormat::Number(fmt) => DatumFormat::Number(fmt.max_width(max_width)),
            DatumFormat::String(fmt) => DatumFormat::String(fmt.max_width(max_width)),
            DatumFormat::Binary(fmt) => DatumFormat::Binary(fmt.max_width(max_width)),
            DatumFormat::Bool(fmt) => DatumFormat::Bool(fmt.max_width(max_width)),
        }
    }

    /// get min width
    pub fn get_min_width(&self) -> Option<usize> {
        match self {
            DatumFormat::Number(fmt) => Some(fmt.min_width),
            DatumFormat::String(fmt) => Some(fmt.min_width),
            DatumFormat::Binary(fmt) => Some(fmt.min_width),
            DatumFormat::Bool(fmt) => Some(fmt.min_width),
        }
    }

    /// get max width
    pub fn get_max_width(&self) -> Option<usize> {
        match self {
            DatumFormat::Number(fmt) => Some(fmt.max_width),
            DatumFormat::String(fmt) => Some(fmt.max_width),
            DatumFormat::Binary(fmt) => Some(fmt.max_width),
            DatumFormat::Bool(fmt) => Some(fmt.max_width),
        }
    }
}

impl TryInto<NumberFormat> for DatumFormat {
    type Error = FormatError;

    fn try_into(self) -> Result<NumberFormat, FormatError> {
        match self {
            DatumFormat::Number(format) => Ok(format),
            _ => Err(FormatError::MismatchedFormatType("not a NumberFormat".to_string())),
        }
    }
}

impl TryInto<StringFormat> for DatumFormat {
    type Error = FormatError;

    fn try_into(self) -> Result<StringFormat, FormatError> {
        match self {
            DatumFormat::String(format) => Ok(format),
            _ => Err(FormatError::MismatchedFormatType("not a StringFormat".to_string())),
        }
    }
}

impl TryInto<BinaryFormat> for DatumFormat {
    type Error = FormatError;

    fn try_into(self) -> Result<BinaryFormat, FormatError> {
        match self {
            DatumFormat::Binary(format) => Ok(format),
            _ => Err(FormatError::MismatchedFormatType("not a BinaryFormat".to_string())),
        }
    }
}

impl TryInto<BoolFormat> for DatumFormat {
    type Error = FormatError;

    fn try_into(self) -> Result<BoolFormat, FormatError> {
        match self {
            DatumFormat::Bool(format) => Ok(format),
            _ => Err(FormatError::MismatchedFormatType("not a BoolFormat".to_string())),
        }
    }
}
