"""
Data visualization tools for SuperNova AI.
"""

import os
import io
import base64
from typing import Optional, Dict, Any, List, Union
import pandas as pd
from ..config.env import DEBUG

# Check for visualization libraries
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

class DataVisualizer:
    """Data visualization tool for creating charts and graphs."""

    def __init__(self):
        """Initialize the data visualization tool."""
        self.output_dir = os.path.join(os.getcwd(), "output", "visualizations")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set default style for matplotlib
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('dark_background')
            sns.set_style("darkgrid")

    def create_visualization(self, data: Union[str, pd.DataFrame], chart_type: str, 
                            x_column: Optional[str] = None, y_column: Optional[str] = None,
                            color_column: Optional[str] = None, title: Optional[str] = None,
                            interactive: bool = True) -> Dict[str, Any]:
        """
        Create a data visualization.

        Args:
            data: CSV string or pandas DataFrame
            chart_type: Type of chart to create (bar, line, scatter, pie, heatmap)
            x_column: Column to use for x-axis
            y_column: Column to use for y-axis
            color_column: Column to use for color
            title: Chart title
            interactive: Whether to create an interactive chart

        Returns:
            Dictionary containing visualization information
        """
        # Convert data to DataFrame if it's a string
        if isinstance(data, str):
            try:
                data = pd.read_csv(io.StringIO(data))
            except Exception as e:
                if DEBUG:
                    print(f"Error parsing CSV data: {e}")
                return {"error": f"Failed to parse CSV data: {str(e)}"}
        
        # Validate data
        if not isinstance(data, pd.DataFrame):
            return {"error": "Data must be a pandas DataFrame or CSV string"}
        
        if data.empty:
            return {"error": "DataFrame is empty"}
        
        # Print debug information
        if DEBUG:
            print(f"Creating {chart_type} chart")
            print(f"Data shape: {data.shape}")
            print(f"Columns: {data.columns.tolist()}")
            print(f"X column: {x_column}")
            print(f"Y column: {y_column}")
            print(f"Color column: {color_column}")
            print(f"Title: {title}")
            print(f"Interactive: {interactive}")
            print(f"Matplotlib available: {MATPLOTLIB_AVAILABLE}")
            print(f"Plotly available: {PLOTLY_AVAILABLE}")
        
        # Use appropriate visualization library
        if interactive and PLOTLY_AVAILABLE:
            return self._create_plotly_chart(data, chart_type, x_column, y_column, color_column, title)
        elif MATPLOTLIB_AVAILABLE:
            return self._create_matplotlib_chart(data, chart_type, x_column, y_column, color_column, title)
        else:
            return {"error": "No visualization libraries available"}

    def _create_plotly_chart(self, data: pd.DataFrame, chart_type: str, 
                           x_column: Optional[str], y_column: Optional[str],
                           color_column: Optional[str], title: Optional[str]) -> Dict[str, Any]:
        """
        Create an interactive chart using Plotly.
        
        Args:
            data: DataFrame containing the data
            chart_type: Type of chart to create
            x_column: Column to use for x-axis
            y_column: Column to use for y-axis
            color_column: Column to use for color
            title: Chart title
            
        Returns:
            Dictionary containing visualization information
        """
        try:
            # Set default columns if not provided
            if x_column is None:
                x_column = data.columns[0]
            
            if y_column is None and len(data.columns) > 1:
                y_column = data.columns[1]
            
            # Create figure based on chart type
            fig = None
            
            if chart_type.lower() == "bar":
                fig = px.bar(data, x=x_column, y=y_column, color=color_column, 
                            title=title, template="plotly_dark")
            
            elif chart_type.lower() == "line":
                fig = px.line(data, x=x_column, y=y_column, color=color_column, 
                             title=title, template="plotly_dark")
            
            elif chart_type.lower() == "scatter":
                fig = px.scatter(data, x=x_column, y=y_column, color=color_column, 
                                title=title, template="plotly_dark")
            
            elif chart_type.lower() == "pie":
                fig = px.pie(data, names=x_column, values=y_column, 
                            title=title, template="plotly_dark")
            
            elif chart_type.lower() == "heatmap":
                # For heatmap, pivot the data if necessary
                if len(data.columns) >= 3 and x_column and y_column and color_column:
                    pivot_data = data.pivot(index=y_column, columns=x_column, values=color_column)
                    fig = px.imshow(pivot_data, title=title, template="plotly_dark")
                else:
                    # Use correlation matrix if not enough columns specified
                    corr_matrix = data.corr()
                    fig = px.imshow(corr_matrix, title=title or "Correlation Matrix", 
                                   template="plotly_dark")
            
            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            # Update layout
            fig.update_layout(
                paper_bgcolor="#343541",
                plot_bgcolor="#444654",
                font=dict(color="#ececf1")
            )
            
            # Save as HTML
            output_path = os.path.join(self.output_dir, f"plotly_{chart_type}.html")
            fig.write_html(output_path)
            
            # Convert to JSON for embedding
            chart_json = fig.to_json()
            
            return {
                "type": chart_type,
                "library": "plotly",
                "path": output_path,
                "title": title,
                "data_shape": data.shape,
                "json": chart_json,
                "interactive": True
            }
        
        except Exception as e:
            if DEBUG:
                print(f"Error creating Plotly chart: {e}")
            
            # Fall back to matplotlib
            if MATPLOTLIB_AVAILABLE:
                return self._create_matplotlib_chart(data, chart_type, x_column, y_column, color_column, title)
            else:
                return {"error": f"Failed to create Plotly chart: {str(e)}"}

    def _create_matplotlib_chart(self, data: pd.DataFrame, chart_type: str, 
                               x_column: Optional[str], y_column: Optional[str],
                               color_column: Optional[str], title: Optional[str]) -> Dict[str, Any]:
        """
        Create a static chart using Matplotlib.
        
        Args:
            data: DataFrame containing the data
            chart_type: Type of chart to create
            x_column: Column to use for x-axis
            y_column: Column to use for y-axis
            color_column: Column to use for color
            title: Chart title
            
        Returns:
            Dictionary containing visualization information
        """
        try:
            # Set default columns if not provided
            if x_column is None:
                x_column = data.columns[0]
            
            if y_column is None and len(data.columns) > 1:
                y_column = data.columns[1]
            
            # Create figure and axes
            plt.figure(figsize=(10, 6), facecolor="#343541")
            ax = plt.gca()
            ax.set_facecolor("#444654")
            
            # Create chart based on type
            if chart_type.lower() == "bar":
                if color_column and color_column in data.columns:
                    # Group by color column
                    grouped = data.groupby(color_column)
                    for name, group in grouped:
                        group.plot(kind="bar", x=x_column, y=y_column, ax=ax, label=name)
                else:
                    data.plot(kind="bar", x=x_column, y=y_column, ax=ax)
            
            elif chart_type.lower() == "line":
                if color_column and color_column in data.columns:
                    # Group by color column
                    grouped = data.groupby(color_column)
                    for name, group in grouped:
                        group.plot(kind="line", x=x_column, y=y_column, ax=ax, label=name)
                else:
                    data.plot(kind="line", x=x_column, y=y_column, ax=ax)
            
            elif chart_type.lower() == "scatter":
                if color_column and color_column in data.columns:
                    # Use seaborn for better scatter plots with categories
                    sns.scatterplot(data=data, x=x_column, y=y_column, hue=color_column, ax=ax)
                else:
                    data.plot(kind="scatter", x=x_column, y=y_column, ax=ax)
            
            elif chart_type.lower() == "pie":
                if y_column:
                    data.plot(kind="pie", y=y_column, labels=data[x_column], ax=ax)
                else:
                    # If no y_column specified, use value counts of x_column
                    data[x_column].value_counts().plot(kind="pie", ax=ax)
            
            elif chart_type.lower() == "heatmap":
                # For heatmap, use correlation matrix if not enough columns specified
                if len(data.columns) >= 3 and x_column and y_column and color_column:
                    pivot_data = data.pivot(index=y_column, columns=x_column, values=color_column)
                    sns.heatmap(pivot_data, annot=True, cmap="viridis", ax=ax)
                else:
                    # Use correlation matrix
                    corr_matrix = data.corr()
                    sns.heatmap(corr_matrix, annot=True, cmap="viridis", ax=ax)
            
            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            # Set title and style
            plt.title(title or f"{chart_type.capitalize()} Chart", color="#ececf1")
            plt.xlabel(x_column, color="#ececf1")
            if y_column:
                plt.ylabel(y_column, color="#ececf1")
            
            # Style the chart
            plt.grid(True, linestyle="--", alpha=0.7)
            plt.tick_params(colors="#ececf1")
            for spine in ax.spines.values():
                spine.set_color("#8e8ea0")
            
            if ax.legend_:
                ax.legend_.set_frame_on(True)
                ax.legend_.get_frame().set_facecolor("#343541")
                ax.legend_.get_frame().set_edgecolor("#8e8ea0")
                for text in ax.legend_.get_texts():
                    text.set_color("#ececf1")
            
            # Save the figure
            output_path = os.path.join(self.output_dir, f"matplotlib_{chart_type}.png")
            plt.tight_layout()
            plt.savefig(output_path, facecolor="#343541", edgecolor="none")
            
            # Convert to base64 for embedding
            with open(output_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode("utf-8")
            
            # Close the figure to free memory
            plt.close()
            
            return {
                "type": chart_type,
                "library": "matplotlib",
                "path": output_path,
                "title": title,
                "data_shape": data.shape,
                "base64": img_data,
                "interactive": False
            }
        
        except Exception as e:
            if DEBUG:
                print(f"Error creating Matplotlib chart: {e}")
            return {"error": f"Failed to create Matplotlib chart: {str(e)}"}

    def parse_csv(self, csv_data: str) -> Dict[str, Any]:
        """
        Parse CSV data and return summary information.
        
        Args:
            csv_data: CSV string
            
        Returns:
            Dictionary containing data summary
        """
        try:
            # Parse CSV
            df = pd.read_csv(io.StringIO(csv_data))
            
            # Generate summary
            summary = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "head": df.head(5).to_dict(orient="records"),
                "describe": df.describe().to_dict(),
                "missing": df.isnull().sum().to_dict()
            }
            
            return {
                "success": True,
                "summary": summary,
                "dataframe": df
            }
        
        except Exception as e:
            if DEBUG:
                print(f"Error parsing CSV data: {e}")
            return {
                "success": False,
                "error": f"Failed to parse CSV data: {str(e)}"
            }

# Create a singleton instance
data_visualizer = DataVisualizer()
