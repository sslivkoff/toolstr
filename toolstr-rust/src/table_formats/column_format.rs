use crate::{
    width, BinaryFormat, BoolFormat, CellFormat, CellFormatShorthand, ColumnData, ColumnType,
    FormatError, NumberFormat, StringFormat, UnknownFormat,
};
// use unicode_truncate::{Alignment, UnicodeTruncateStr};

/// column format shorthand
#[derive(Debug, Clone)]
pub struct ColumnFormatShorthand {
    /// name
    pub name: String,
    /// display name
    pub display_name: String,
    /// format
    pub format: CellFormatShorthand,
    /// horizontal alignment
    pub horizontal_align: HorizontalAlign,
    /// vertical alignment
    pub vertical_align: VerticalAlign,
}

impl ColumnFormatShorthand {
    /// finalize shorthand into format format
    pub fn finalize(self, column_type: &ColumnType) -> Result<ColumnFormat, FormatError> {
        Ok(ColumnFormat {
            name: self.name,
            display_name: self.display_name,
            format: self.format.finalize(column_type)?,
            horizontal_align: self.horizontal_align,
            vertical_align: self.vertical_align,
        })
    }
}

impl Default for ColumnFormatShorthand {
    fn default() -> ColumnFormatShorthand {
        let format = UnknownFormat {
            min_width: None,
            max_width: None,
        };
        ColumnFormatShorthand {
            name: "".to_string(),
            display_name: "".to_string(),
            format: CellFormatShorthand::Unknown(format),
            horizontal_align: HorizontalAlign::Right,
            vertical_align: VerticalAlign::Top,
        }
    }
}

/// column format
#[derive(Debug, Clone)]
pub struct ColumnFormat {
    /// name
    pub name: String,
    /// display name
    pub display_name: String,
    /// format
    pub format: CellFormat,
    /// horizontal alignment
    pub horizontal_align: HorizontalAlign,
    /// vertical alignment
    pub vertical_align: VerticalAlign,
}

/// horizontal alignment
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HorizontalAlign {
    /// left
    Left,
    /// right
    Right,
}

/// vertical alignment
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VerticalAlign {
    /// top
    Top,
    /// bottom
    Bottom,
}

impl ColumnFormat {
    /// get header width
    pub fn header_width(&self) -> usize {
        width(&self.display_name)
    }

    /// get min width
    pub fn get_min_width(&self) -> usize {
        self.format.get_min_width().unwrap_or(0)
    }

    /// get max width
    pub fn get_max_width(&self) -> usize {
        self.format.get_max_width().unwrap_or(usize::MAX)
    }

    /// format series
    pub fn format(&self, series: &ColumnData) -> Result<Vec<String>, FormatError> {
        let formatted: Result<Vec<String>, FormatError> = match series {
            ColumnData::BinaryColumn(value) => {
                let fmt: BinaryFormat = self.format.clone().try_into()?;
                value.iter().map(|v| fmt.format(v)).collect()
            }
            ColumnData::BinaryOptionColumn(value) => {
                let fmt: BinaryFormat = self.format.clone().try_into()?;
                value
                    .iter()
                    .map(|v| fmt.format_option(v, fmt.fill_char.to_string().repeat(fmt.min_width)))
                    .collect()
            }
            ColumnData::FloatColumn(value) => {
                let fmt: NumberFormat = self.format.clone().try_into()?;
                value.iter().map(|v| fmt.format(*v)).collect()
            }
            ColumnData::FloatOptionColumn(value) => {
                let fmt: NumberFormat = self.format.clone().try_into()?;
                value
                    .iter()
                    .map(|v| fmt.format_option(*v, fmt.fill.to_string().repeat(fmt.min_width)))
                    .collect()
            }
            ColumnData::IntegerColumn(value) => {
                let fmt: NumberFormat = self.format.clone().try_into()?;
                value.iter().map(|v| fmt.format(*v)).collect()
            }
            ColumnData::IntegerOptionColumn(value) => {
                let fmt: NumberFormat = self.format.clone().try_into()?;
                value
                    .iter()
                    .map(|v| fmt.format_option(*v, fmt.fill.to_string().repeat(fmt.min_width)))
                    .collect()
            }
            ColumnData::StringColumn(value) => {
                let fmt: StringFormat = self.format.clone().try_into()?;
                value.iter().map(|v| fmt.format(v)).collect()
            }
            ColumnData::StringOptionColumn(value) => {
                let fmt: StringFormat = self.format.clone().try_into()?;
                value
                    .iter()
                    .map(|v| {
                        fmt.format_option(
                            v.clone(),
                            fmt.fill_char.to_string().repeat(fmt.min_width),
                        )
                    })
                    .collect()
            }
            ColumnData::BoolColumn(value) => {
                let fmt: BoolFormat = self.format.clone().try_into()?;
                value.iter().map(|v| fmt.format(*v)).collect()
            }
            ColumnData::BoolOptionColumn(value) => {
                let fmt: BoolFormat = self.format.clone().try_into()?;
                value
                    .iter()
                    .map(|v| fmt.format_option(*v, fmt.fill_char.to_string().repeat(fmt.min_width)))
                    .collect()
            }
        };
        let formatted = formatted?;

        // let max_width = formatted.iter().map(width).max().unwrap_or(0);

        // let formatted = if self.horizontal_align == HorizontalAlign::Right {
        //     formatted
        //         .into_iter()
        //         // .map(|s| s.unicode_pad(max_width, Alignment::Right, true).to_string())
        //         .collect()
        // } else {
        //     formatted
        //         .into_iter()
        //         // .map(|s| s.unicode_pad(max_width, Alignment::Left, true).to_string())
        //         .collect()
        // };

        Ok(formatted)
    }
}

// builder
impl ColumnFormat {
    /// set name
    pub fn name<T: AsRef<str>>(mut self, name: T) -> ColumnFormat {
        let name = name.as_ref().to_string();
        self.name = name.clone();
        if self.display_name.is_empty() {
            self.display_name = name
        };
        self
    }

    /// set display name
    pub fn display_name<T: AsRef<str>>(mut self, display_name: T) -> ColumnFormat {
        self.display_name = display_name.as_ref().to_string();
        self
    }

    /// set newline underscores
    pub fn newline_underscores(mut self) -> ColumnFormat {
        self.display_name = self.display_name.replace('_', "\n");
        self
    }

    /// set width
    pub fn width(self, width: usize) -> ColumnFormat {
        self.min_width(width).max_width(width)
    }

    /// set min width
    pub fn min_width(mut self, width: usize) -> ColumnFormat {
        self.format = self.format.min_width(width);
        self
    }

    /// set max width
    pub fn max_width(mut self, width: usize) -> ColumnFormat {
        self.format = self.format.max_width(width);
        self
    }
}

// builder
impl ColumnFormatShorthand {
    /// new
    pub fn new() -> ColumnFormatShorthand {
        ColumnFormatShorthand::default()
    }

    /// set name
    pub fn name<T: AsRef<str>>(mut self, name: T) -> ColumnFormatShorthand {
        let name = name.as_ref().to_string();
        self.name = name.clone();
        if self.display_name.is_empty() {
            self.display_name = name
        };
        self
    }

    /// set display name
    pub fn display_name<T: AsRef<str>>(mut self, display_name: T) -> ColumnFormatShorthand {
        self.display_name = display_name.as_ref().to_string();
        self
    }

    /// set newline underscores
    pub fn newline_underscores(mut self) -> ColumnFormatShorthand {
        self.display_name = self.display_name.replace('_', "\n");
        self
    }

    /// set width
    pub fn width(self, width: usize) -> ColumnFormatShorthand {
        self.min_width(width).max_width(width)
    }

    /// set min width
    pub fn min_width(mut self, width: usize) -> ColumnFormatShorthand {
        self.format = self.format.min_width(width);
        self
    }

    /// set max width
    pub fn max_width(mut self, width: usize) -> ColumnFormatShorthand {
        self.format = self.format.max_width(width);
        self
    }

    /// set format
    pub fn set_format<T: Into<CellFormatShorthand>>(mut self, format: T) -> ColumnFormatShorthand {
        self.format = format.into();
        self
    }
}
