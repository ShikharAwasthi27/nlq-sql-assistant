import streamlit as st
import pandas as pd

from sql_generator import generate_sql
from guardrails import validate_sql, SQLValidationError
from database import execute_query
from logger_util import (
    log_interaction,
    initialize_logs
)


st.set_page_config(
    page_title="NLQ-to-SQL Assistant",
    page_icon="📊",
    layout="wide"
)


initialize_logs()


if "query_history" not in st.session_state:
    st.session_state.query_history = []


st.title("📊 Natural Language → SQL Analytics Assistant")

st.markdown(
    """
Ask business questions in plain English and get
SQL-driven insights instantly.
"""
)


with st.sidebar:
    st.header("Query History")

    if st.session_state.query_history:
        for i, query in enumerate(
            reversed(st.session_state.query_history),
            start=1
        ):
            st.write(f"{i}. {query}")

    else:
        st.info("No queries asked yet.")


question = st.text_input(
    "Enter your business question:",
    placeholder="Example: What are the top selling products?"
)


if st.button("Generate Insights"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    st.session_state.query_history.append(question)

    try:

        # -----------------------------------
        # Step 1: Generate SQL
        # -----------------------------------

        with st.spinner("Generating SQL using Gemini..."):

            generated_output = generate_sql(
                question
            )

        sql = generated_output["sql"]
        explanation = generated_output["explanation"]

        st.subheader("Generated SQL")

        st.code(
            sql,
            language="sql"
        )

        st.subheader("Explanation")

        st.write(explanation)

        # -----------------------------------
        # Step 2: Validate SQL
        # -----------------------------------

        try:
            validate_sql(sql)

            validation_status = "ALLOWED"

            st.success(
                "SQL validation passed."
            )

        except SQLValidationError as e:

            validation_status = "BLOCKED"

            st.error(
                f"Validation Failed: {str(e)}"
            )

            log_interaction(
                question=question,
                sql=sql,
                validation_status=validation_status,
                execution_time=0,
                rows_returned=0,
                error_message=str(e)
            )

            st.stop()

        # -----------------------------------
        # Step 3: Execute SQL
        # -----------------------------------

        with st.spinner("Executing query..."):

            success, result, execution_time = (
                execute_query(sql)
            )

        if success:

            st.subheader("Results")

            st.dataframe(
                result,
                use_container_width=True
            )

            st.info(
                f"Execution Time: "
                f"{execution_time:.2f} seconds"
            )

            log_interaction(
                question=question,
                sql=sql,
                validation_status=validation_status,
                execution_time=execution_time,
                rows_returned=len(result),
                error_message=""
            )

        else:

            st.error(
                f"Execution Failed: {result}"
            )

            log_interaction(
                question=question,
                sql=sql,
                validation_status=validation_status,
                execution_time=execution_time,
                rows_returned=0,
                error_message=result
            )

    except Exception as e:

        st.error(
            f"Unexpected Error: {str(e)}"
        )

        log_interaction(
            question=question,
            sql="",
            validation_status="ERROR",
            execution_time=0,
            rows_returned=0,
            error_message=str(e)
        )
