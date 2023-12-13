use crate::{Column, ColumnFormat, ColumnFormatShorthand, FormatError, Table};

const DEFAULT_TABLE_HEIGHT: usize = 30;

/// dataframe format
#[derive(Debug)]
pub struct TableFormat {
    /// column formats
    pub column_formats: Option<Vec<ColumnFormatShorthand>>,
    /// column delimiter
    pub column_delimiter: String,
    /// header separator delimiter
    pub header_separator_delimiter: String,
    /// header separator char
    pub header_separator_char: char,
    /// include header row
    pub include_header_row: bool,
    /// include header separator row
    pub include_header_separator_row: bool,
    /// include summary row
    pub include_summary_row: bool,
    /// include summary separator row
    pub include_summary_separator_row: bool,
    /// render height
    pub render_height: Option<usize>,
    /// max render width
    pub max_render_width: Option<usize>,
    /// indent
    pub indent: usize,
}

impl Default for TableFormat {
    fn default() -> TableFormat {
        TableFormat {
            column_formats: None,
            column_delimiter: "  │  ".to_string(),
            header_separator_delimiter: "──┼──".to_string(),
            header_separator_char: '─',
            include_header_row: true,
            include_header_separator_row: true,
            include_summary_row: false,
            include_summary_separator_row: false,
            render_height: None,
            max_render_width: None,
            indent: 0,
        }
    }
}

/// finalized TableFormat
#[derive(Debug)]
pub struct TableFormatFinal {
    /// column formats
    pub column_formats: Vec<ColumnFormat>,
    /// column delimiter
    pub column_delimiter: String,
    /// header separator delimiter
    pub header_separator_delimiter: String,
    /// header separator char
    pub header_separator_char: char,
    /// include header row
    pub include_header_row: bool,
    /// include header separator row
    pub include_header_separator_row: bool,
    /// include summary row
    pub include_summary_row: bool,
    /// include summary separator row
    pub include_summary_separator_row: bool,
    /// render height
    pub render_height: usize,
    /// max render width
    pub max_render_width: usize,
    /// indent
    pub indent: usize,
}

impl TableFormat {
    /// format dataframe as String
    pub fn print(&self, df: Table) -> Result<(), FormatError> {
        let fmt = self.finalize(df.clone())?;
        println!("{}", fmt.format(df)?);
        Ok(())
    }

    /// format dataframe as String
    pub fn format(&self, df: Table) -> Result<String, FormatError> {
        let fmt = self.finalize(df.clone())?;
        fmt.format(df)
    }

    /// fill missing format information based on dataframe
    fn finalize(&self, table: Table) -> Result<TableFormatFinal, FormatError> {
        let column_formats: Vec<ColumnFormat> = match &self.column_formats {
            Some(column_formats) => {
                let mut fmts = Vec::new();
                for (col_format, col) in column_formats.iter().zip(table.columns.iter()) {
                    fmts.push(col_format.clone().finalize(&col.data.column_type())?);
                }
                fmts
            }
            None => {
                let fmts: Result<Vec<ColumnFormat>, FormatError> = table
                    .columns
                    .iter()
                    .map(|column| {
                        ColumnFormatShorthand::new()
                            .name(column.name.clone())
                            .finalize(&column.data.column_type())
                    })
                    .collect();
                fmts?
            }
        };

        let max_render_width = match self.max_render_width {
            Some(value) => value,
            None => {
                let max_render_width = safe_sum_with_max_on_overflow(
                    column_formats.iter().map(|c| c.get_max_width()).collect(),
                );
                safe_sum_with_max_on_overflow(vec![
                    max_render_width,
                    self.column_delimiter.chars().count() * (column_formats.len() - 1),
                ])
            }
        };
        let fmt = TableFormatFinal {
            column_formats,
            column_delimiter: self.column_delimiter.clone(),
            header_separator_delimiter: self.header_separator_delimiter.clone(),
            header_separator_char: self.header_separator_char,
            include_header_row: self.include_header_row,
            include_header_separator_row: self.include_header_separator_row,
            include_summary_row: self.include_summary_row,
            include_summary_separator_row: self.include_summary_separator_row,
            render_height: self.render_height.unwrap_or(DEFAULT_TABLE_HEIGHT),
            max_render_width,
            indent: self.indent,
        };
        Ok(fmt)
    }
}

fn safe_sum_with_max_on_overflow(numbers: Vec<usize>) -> usize {
    let mut sum: usize = 0;
    for number in numbers {
        match sum.checked_add(number) {
            Some(s) => sum = s,
            None => return usize::MAX,
        };
    }
    sum
}

// get number of lines in header
impl TableFormatFinal {
    fn n_header_lines(&self) -> usize {
        // TODO: take an n_used_columns parameter, for if only subset of columns used
        self.column_formats
            .iter()
            .map(|f| f.display_name.chars().filter(|&c| c == '\n').count() + 1)
            .max()
            .unwrap_or(0)
    }

    fn n_data_rows(&self) -> usize {
        self.render_height
            - (self.include_header_row as usize)
                * (self.n_header_lines() + (self.include_header_separator_row as usize))
            - (self.include_summary_row as usize)
                * (1 + (self.include_summary_separator_row as usize))
    }

    fn total_rendered_width(&self, used_widths: &[usize]) -> usize {
        used_widths.iter().sum::<usize>()
            + ((used_widths.len() as i64 - 1).max(0) as usize)
                * self.column_delimiter.chars().count()
    }

    fn render_header_rows(&self, used_widths: &[usize], total_width: usize) -> Vec<String> {
        let n_header_lines = self.n_header_lines();
        let mut rows: Vec<String> = (0..n_header_lines)
            .map(|_| String::with_capacity(total_width))
            .collect();
        for (c, width) in used_widths.iter().enumerate() {
            if c != 0 {
                for row in rows.iter_mut() {
                    row.push_str(self.column_delimiter.as_str());
                }
            }
            let name = self.column_formats[c].display_name.as_str();
            let lines: Vec<String> = name.split('\n').map(|s| s.to_string()).collect();
            let bound = n_header_lines - lines.len();
            for row in rows.iter_mut().take(bound) {
                row.push_str(" ".repeat(*width).as_str());
            }
            for (row, line) in rows.iter_mut().skip(bound).zip(lines) {
                row.push_str(format!("{:>width$}", line, width = width).as_str());
            }
        }

        rows
    }

    fn render_header_separator_row(&self, used_widths: &[usize], total_width: usize) -> String {
        let mut row = String::with_capacity(total_width);
        let separator = self.header_separator_char.to_string();
        for (c, width) in used_widths.iter().enumerate() {
            if c != 0 {
                row.push_str(self.header_separator_delimiter.as_str());
            }
            row.push_str(separator.repeat(*width).as_str());
        }
        row
    }

    fn render_columns(&self, df: Table) -> Result<(Vec<usize>, Vec<Vec<String>>), FormatError> {
        // compute global sizes
        let mut column_min_widths: Vec<usize> = vec![];
        let mut column_max_widths: Vec<usize> = vec![];
        for fmt in self.column_formats.iter() {
            let min_width = fmt.header_width().max(fmt.get_min_width());
            let max_width = fmt.get_max_width();
            if min_width > max_width {
                let msg = format!("min_width > max_width for column: {}", fmt.display_name);
                return Err(FormatError::InvalidFormat(msg));
            }
            column_min_widths.push(min_width);
            column_max_widths.push(max_width);
        }

        let total_min_width = column_min_widths.iter().sum::<usize>()
            + self.column_delimiter.chars().count() * (self.column_formats.len() - 1);
        // let total_max_width = column_max_widths.iter().sum::<usize>();

        // compute how many columns to include
        let n_used_columns = if total_min_width >= self.max_render_width {
            let mut n_used_columns = 0;
            let mut used_width = 0;
            for min_width in column_min_widths.iter() {
                if used_width > 0 {
                    used_width += self.column_delimiter.chars().count();
                }
                if used_width + min_width <= self.max_render_width {
                    n_used_columns += 1;
                    used_width += min_width;
                } else {
                    break;
                }
            }
            n_used_columns
        } else {
            self.column_formats.len()
        };
        // let column_min_widths = column_min_widths.into_iter().take(n_used_columns);
        // let column_max_widths = column_max_widths.into_iter().take(n_used_columns);

        // compute used widths
        let mut columns = Vec::with_capacity(n_used_columns);
        let mut used_widths = Vec::with_capacity(n_used_columns);
        let mut spare_room: usize = self.max_render_width
            - column_min_widths.iter().take(n_used_columns).sum::<usize>()
            - self.column_delimiter.chars().count() * ((n_used_columns as i64 - 1).max(0) as usize);

        // println!("COLUMN_MIN_WIDTHS {:?}", column_min_widths);
        // println!("TOTAL_MIN_WIDTHS {}",
        // column_min_widths.iter().take(n_used_columns).sum::<usize>());
        // println!("SPARE_ROOM {}", spare_room);
        // println!("MAX_RENDER_WIDTH {:?}", self.max_render_width);
        // println!(
        //     "MIN_TOTAL_W_DELIM {:?}",
        //     column_min_widths.iter().take(n_used_columns).sum::<usize>()
        //         + self.column_delimiter.chars().count()
        //             * ((n_used_columns as i64 - 1).max(0) as usize)
        // );
        // println!();

        for (c, column_format) in self.column_formats.iter().take(n_used_columns).enumerate() {
            if let Some(0) = df.n_rows {
                used_widths.push(column_min_widths[c]);
                columns.push(vec![]);
                continue;
            }

            let min_width = column_min_widths[c];
            let max_width = column_max_widths[c].min(min_width + spare_room);
            let name = column_format.name.clone();
            let column = column_format
                .clone()
                .min_width(min_width)
                .max_width(max_width)
                .format(df.column(name)?.data.as_ref())?;
            let used_width = column
                .iter()
                .map(|s| s.chars().count())
                // .map(|s| unicode_width::UnicodeWidthStr::width_cjk(s.as_str()))
                // .map(|s| unicode_width::UnicodeWidthStr::width(s.as_str()))
                .max()
                .ok_or(FormatError::EmptyData(format!(
                    "empty column: {}",
                    column_format.name
                )))?;
            let used_width = used_width.max(min_width);

            // println!("COLUMN: {:?}", column.clone());

            columns.push(column);

            // println!("NAME {}", column_format.name);
            // println!("FORMAT {:?}", column_format);
            // println!("MAX_WIDTH {}", max_width);
            // println!("MIN_WIDTH {}", min_width);
            // println!("SPARE_ROOM {}", spare_room);
            // println!("USED_WIDTH {}", used_width);
            // println!("NEW_SPARE_ROOM {}", spare_room - (used_width - min_width));
            // println!();

            used_widths.push(used_width);
            spare_room -= used_width - min_width;
        }
        Ok((used_widths, columns))
    }

    fn assemble_rows(&self, columns: Vec<Vec<String>>, rows: &mut Vec<String>, total_width: usize) {
        let n_data_rows = match columns.first() {
            Some(column) => column.len(),
            None => return,
        };
        // println!("N_DATA_ROWS: {}", n_data_rows);
        for r in 0..n_data_rows {
            let mut row = String::with_capacity(total_width);
            for (c, column) in columns.iter().enumerate() {
                if c != 0 {
                    row.push_str(self.column_delimiter.as_str())
                }
                row.push_str(column[r].as_str())
            }
            rows.push(row)
        }
    }

    pub(crate) fn format(&self, table: Table) -> Result<String, FormatError> {
        // clip
        let n_data_rows = self.n_data_rows();
        let columns: Vec<Column> = table.columns.into_iter().take(n_data_rows).collect();
        let table = Table { columns, ..table };

        // render columns
        let (used_widths, columns) = self.render_columns(table)?;
        let total_width = self.total_rendered_width(&used_widths);

        // assemble rows
        let mut rows = Vec::with_capacity(self.render_height);
        if self.include_header_row {
            for row in self.render_header_rows(&used_widths, total_width) {
                rows.push(row);
            }
            if self.include_header_separator_row {
                rows.push(self.render_header_separator_row(&used_widths, total_width));
            }
        };
        self.assemble_rows(columns, &mut rows, total_width);
        if self.include_summary_row {
            todo!("summary row")
        }

        let rows = if self.indent > 0 {
            let indent = " ".repeat(self.indent);
            rows.into_iter()
                .map(|row| format!("{}{}", indent, row))
                .collect()
        } else {
            rows
        };

        Ok(rows.join("\n"))
    }
}
