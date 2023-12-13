use crate::FormatError;
use std::sync::Arc;

/// Table for printing
#[derive(Debug, Clone, Default)]
pub struct Table {
    /// number of rows in table
    pub n_rows: Option<usize>,
    /// columns
    pub columns: Vec<Column>,
}

impl Table {
    /// create new table
    pub fn new() -> Table {
        Table {
            n_rows: None,
            columns: Vec::new(),
        }
    }

    /// add column to table
    pub fn add_column<T: Into<ColumnData>, S: AsRef<str>>(
        &mut self,
        name: S,
        data: T,
    ) -> Result<(), FormatError> {
        let column = Column::new(name.as_ref().to_string(), data);
        if let Some(n_rows) = self.n_rows {
            if n_rows != column.data.len() {
                return Err(FormatError::DifferentRowCounts);
            }
        } else {
            self.n_rows = Some(column.data.len());
        }
        self.columns.push(column);
        Ok(())
    }

    /// get column by name
    pub fn column(&self, name: String) -> Result<Column, FormatError> {
        for column in self.columns.iter() {
            if name == column.name {
                return Ok(column.clone());
            }
        }
        Err(FormatError::ColumnMissing(format!(
            "column missing: {}",
            name
        )))
    }
}

/// column for printing
#[derive(Debug, Clone)]
pub struct Column {
    /// name of column
    pub name: String,
    /// data of column
    pub data: Arc<ColumnData>,
}

impl Column {
    fn new<T: Into<ColumnData>>(name: String, data: T) -> Column {
        Column {
            name,
            data: Arc::new(data.into()),
        }
    }
}

/// Column Type
#[derive(Clone, Debug)]
pub enum ColumnType {
    /// binary
    Binary,
    /// string
    String,
    /// bool
    Bool,
    /// float
    Float,
    /// integer
    Integer,
}

/// Column Vec
#[derive(Clone, Debug)]
pub enum ColumnData {
    /// binary column
    BinaryColumn(Vec<Vec<u8>>),
    /// string column
    StringColumn(Vec<String>),
    /// bool column
    BoolColumn(Vec<bool>),
    /// integer column (stored as f64 for formatting)
    IntegerColumn(Vec<f64>),
    /// float column
    FloatColumn(Vec<f64>),
    /// binary option column
    BinaryOptionColumn(Vec<Option<Vec<u8>>>),
    /// string option column
    StringOptionColumn(Vec<Option<String>>),
    /// bool option column
    BoolOptionColumn(Vec<Option<bool>>),
    /// integer option column
    IntegerOptionColumn(Vec<Option<f64>>),
    /// float option column
    FloatOptionColumn(Vec<Option<f64>>),
}

impl ColumnData {
    /// len of column data
    pub fn len(&self) -> usize {
        match self {
            ColumnData::BinaryColumn(value) => value.len(),
            ColumnData::StringColumn(value) => value.len(),
            ColumnData::BoolColumn(value) => value.len(),
            ColumnData::IntegerColumn(value) => value.len(),
            ColumnData::FloatColumn(value) => value.len(),
            ColumnData::BinaryOptionColumn(value) => value.len(),
            ColumnData::StringOptionColumn(value) => value.len(),
            ColumnData::BoolOptionColumn(value) => value.len(),
            ColumnData::IntegerOptionColumn(value) => value.len(),
            ColumnData::FloatOptionColumn(value) => value.len(),
        }
    }

    /// is_empty() of column data
    pub fn is_empty(&self) -> bool {
        match self {
            ColumnData::BinaryColumn(value) => value.is_empty(),
            ColumnData::StringColumn(value) => value.is_empty(),
            ColumnData::BoolColumn(value) => value.is_empty(),
            ColumnData::IntegerColumn(value) => value.is_empty(),
            ColumnData::FloatColumn(value) => value.is_empty(),
            ColumnData::BinaryOptionColumn(value) => value.is_empty(),
            ColumnData::StringOptionColumn(value) => value.is_empty(),
            ColumnData::BoolOptionColumn(value) => value.is_empty(),
            ColumnData::IntegerOptionColumn(value) => value.is_empty(),
            ColumnData::FloatOptionColumn(value) => value.is_empty(),
        }
    }

    /// column type
    pub fn column_type(&self) -> ColumnType {
        match self {
            ColumnData::BinaryColumn(_) => ColumnType::Binary,
            ColumnData::StringColumn(_) => ColumnType::String,
            ColumnData::BoolColumn(_) => ColumnType::Bool,
            ColumnData::IntegerColumn(_) => ColumnType::Integer,
            ColumnData::FloatColumn(_) => ColumnType::Float,
            ColumnData::BinaryOptionColumn(_) => ColumnType::Binary,
            ColumnData::StringOptionColumn(_) => ColumnType::String,
            ColumnData::BoolOptionColumn(_) => ColumnType::Bool,
            ColumnData::IntegerOptionColumn(_) => ColumnType::Integer,
            ColumnData::FloatOptionColumn(_) => ColumnType::Float,
        }
    }
}

impl From<Vec<Vec<u8>>> for ColumnData {
    fn from(value: Vec<Vec<u8>>) -> Self {
        ColumnData::BinaryColumn(value)
    }
}

impl From<Vec<Option<Vec<u8>>>> for ColumnData {
    fn from(value: Vec<Option<Vec<u8>>>) -> Self {
        ColumnData::BinaryOptionColumn(value)
    }
}

impl From<Vec<String>> for ColumnData {
    fn from(value: Vec<String>) -> Self {
        ColumnData::StringColumn(value)
    }
}

impl From<Vec<Option<String>>> for ColumnData {
    fn from(value: Vec<Option<String>>) -> Self {
        ColumnData::StringOptionColumn(value)
    }
}

impl From<Vec<&str>> for ColumnData {
    fn from(value: Vec<&str>) -> Self {
        ColumnData::StringColumn(value.into_iter().map(|s| s.to_string()).collect())
    }
}

impl From<Vec<Option<&str>>> for ColumnData {
    fn from(value: Vec<Option<&str>>) -> Self {
        ColumnData::StringOptionColumn(
            value
                .into_iter()
                .map(|s| s.map(|s| s.to_string()))
                .collect(),
        )
    }
}

impl From<Vec<bool>> for ColumnData {
    fn from(value: Vec<bool>) -> Self {
        ColumnData::BoolColumn(value)
    }
}

impl From<Vec<Option<bool>>> for ColumnData {
    fn from(value: Vec<Option<bool>>) -> Self {
        ColumnData::BoolOptionColumn(value)
    }
}

impl From<Vec<f32>> for ColumnData {
    fn from(value: Vec<f32>) -> Self {
        ColumnData::FloatColumn(value.into_iter().map(|v| v as f64).collect())
    }
}

impl From<Vec<Option<f32>>> for ColumnData {
    fn from(value: Vec<Option<f32>>) -> Self {
        ColumnData::FloatOptionColumn(
            value
                .into_iter()
                .map(|opt_v| opt_v.map(|v| v as f64))
                .collect(),
        )
    }
}

impl From<Vec<f64>> for ColumnData {
    fn from(value: Vec<f64>) -> Self {
        ColumnData::FloatColumn(value)
    }
}

impl From<Vec<Option<f64>>> for ColumnData {
    fn from(value: Vec<Option<f64>>) -> Self {
        ColumnData::FloatOptionColumn(value)
    }
}

impl From<Vec<u32>> for ColumnData {
    fn from(value: Vec<u32>) -> Self {
        ColumnData::IntegerColumn(value.into_iter().map(|v| v as f64).collect())
    }
}

impl From<Vec<Option<u32>>> for ColumnData {
    fn from(value: Vec<Option<u32>>) -> Self {
        ColumnData::IntegerOptionColumn(
            value
                .into_iter()
                .map(|opt_v| opt_v.map(|v| v as f64))
                .collect(),
        )
    }
}

impl From<Vec<u64>> for ColumnData {
    fn from(value: Vec<u64>) -> Self {
        ColumnData::IntegerColumn(value.into_iter().map(|v| v as f64).collect())
    }
}

impl From<Vec<Option<u64>>> for ColumnData {
    fn from(value: Vec<Option<u64>>) -> Self {
        ColumnData::IntegerOptionColumn(
            value
                .into_iter()
                .map(|opt_v| opt_v.map(|v| v as f64))
                .collect(),
        )
    }
}

impl From<Vec<i32>> for ColumnData {
    fn from(value: Vec<i32>) -> Self {
        ColumnData::IntegerColumn(value.into_iter().map(|v| v as f64).collect())
    }
}

impl From<Vec<Option<i32>>> for ColumnData {
    fn from(value: Vec<Option<i32>>) -> Self {
        ColumnData::IntegerOptionColumn(
            value
                .into_iter()
                .map(|opt_v| opt_v.map(|v| v as f64))
                .collect(),
        )
    }
}

impl From<Vec<i64>> for ColumnData {
    fn from(value: Vec<i64>) -> Self {
        ColumnData::IntegerColumn(value.into_iter().map(|v| v as f64).collect())
    }
}

impl From<Vec<Option<i64>>> for ColumnData {
    fn from(value: Vec<Option<i64>>) -> Self {
        ColumnData::IntegerOptionColumn(
            value
                .into_iter()
                .map(|opt_v| opt_v.map(|v| v as f64))
                .collect(),
        )
    }
}
