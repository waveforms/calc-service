import React, { useState, Fragment } from "react";
import { Formik, Field } from "formik";
import s from "./component/app.component.css";
import * as yup from "yup";


const initialState = {
  parent_node_id: "",
  node_value_display: "",
  node_value: "",
  left_or_right: "",
  number_children: ""
};
const userSchema = yup.object().shape({
  parent_node_id:yup.string().required(),
  node_value: yup.string().required(),
  node_value_display: yup.string().required(),
  left_or_right: yup.string().required(),
  number_children: yup.string(), 
});
function AddUserTreeForm(props) {
  const [user, setUser] = useState(initialState);
  if(user.node_value_display !== ""){
    props.handleValues(user)
  }
  
  return (
    <Fragment> 
      <Formik
        initialValues={user}
        onSubmit={(values, actions) => {
          console.log(actions);
          actions.setSubmitting(true);
          setUser(values);
          setTimeout(() => {
            actions.resetForm(initialState);
            actions.setSubmitting(false);
          }, 2000);
        }}
        validationSchema={userSchema}
      >
        {props =>
          !props.isSubmitting ? (
            <form onSubmit={props.handleSubmit} className={s.form}>
              <Field
                type="parent_node_id"
                placeholder="Enter parent_node_id"
                onChange={props.handleChange}
                name="parent_node_id"
                value={props.values.parent_node_id}
                className={s.text_field}
              />

              {props.errors.parent_node_id && props.touched.parent_node_id ? (
                <span className={s.field_text}>{props.errors.parent_node_id}</span>
              ) : (
                ""
              )}
              <Field
                type="node_value_display"
                placeholder="Enter node_value_display"
                onChange={props.handleChange}
                name="node_value_display"
                value={props.values.node_value_display}
                className={s.text_field}
              />

              {props.errors.node_value_display && props.touched.node_value_display ? (
                <span className={s.field_text}>{props.errors.node_value_display}</span>
              ) : (
                ""
              )}

              <Field
                type="node_value"
                onChange={props.handleChange}
                name="node_value"
                value={props.values.node_value}
                placeholder="node_value"
                className={s.text_field}
              />

              {props.errors.node_value && props.touched.node_value ? (
                <span className={s.field_text}>{props.errors.node_value}</span>
              ) : (
                ""
              )}
              <Field
                name="left_or_right"
                onChange={props.handleChange}
                value={props.values.left_or_right}
                type="text"
                placeholder="left_or_right"
                className={s.text_field}
              />
              {props.errors.left_or_right && props.touched.left_or_right ? (
                <span className={s.field_text}>{props.errors.left_or_right}</span>
              ) : (
                ""
              )}
              <button
                type="submit"
                disabled={!props.dirty && !props.isSubmitting}
                className={`${s.button} ${s.submit_button}`}
              >
                Submit
              </button>
              <button
                disabled={!props.dirty}
                onClick={props.handleReset}
                type="button"
                className={s.button}
              >
                Reset
              </button>
            </form>
          ) : (
            <div className={s.overlay} />
          )
        }
      </Formik>
      <span className="output">{JSON.stringify(user, null, 2)}</span>
    </Fragment>
  );
}
export default AddUserTreeForm;