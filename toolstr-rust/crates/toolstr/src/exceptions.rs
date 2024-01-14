use polars::prelude::PolarsError;
use thiserror::Error;

/// Represents various errors that can occur during formatting operations.
#[derive(Error, Debug)]
pub enum FormatError {
    /// Error indicating that the format type could not be parsed.
    #[error("Could not parse format type")]
    CouldNotParseFormatType,

    /// Error indicating a failure in decomposing the coefficient exponent.
    #[error("Could not decompose coefficient exponent")]
    CouldNotDecomposeCoefficientExponent,

    /// Error indicating a failure in creating a regular expression.
    #[error("Could not create regex")]
    CouldNotCreateRegex,

    /// Error when a regex match could not be performed.
    #[error("Regex could not match")]
    CouldNotMatchRegex,

    /// Error indicating an invalid format, with details.
    #[error("Invalid format: {0}")]
    InvalidFormat(String),

    /// Error indicating that the provided data is empty, with details.
    #[error("Empty data: {0}")]
    EmptyData(String),

    /// Error wrapping a `PolarsError` from the `polars` crate.
    #[error(transparent)]
    PolarsError(#[from] PolarsError),

    /// Error indicating a missing column, with the column's name.
    #[error("Column missing: {0}")]
    ColumnMissing(String),

    /// Error indicating an unsupported datatype, with details.
    #[error("Unsupported datatype: {0}")]
    UnsupportedDatatype(String),

    /// Error for mismatched format types, with details.
    #[error("Mismatched format type: {0}")]
    MismatchedFormatType(String),

    /// Error indicating different numbers of rows for columns in a table.
    #[error("Different numbers of rows for columns in table")]
    DifferentRowCounts,
}
