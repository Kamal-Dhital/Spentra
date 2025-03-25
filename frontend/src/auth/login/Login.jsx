import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import Signup from '../signup/Signup';
import { NavLink, useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate()
  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validationSchema: Yup.object({
      username: Yup.string()
        .min(3, 'Username must be at least 3 characters')
        .required('Username is required'),
      password: Yup.string()
        .min(8, 'Password must be at least 8 characters')
        .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
        .required('Password is required'),
    }),
    onSubmit: (values) => {
      console.log('Form Data:', values);
    },
  });

  return (
    <div className='w-full flex'>
      <section className='flex flex-col w-1/2'>
        <div className='flex justify-center items-center'>
          <img className='w-50' src='logo.png' alt='Logo' />
        </div>

        <div className='flex flex-col gap-5 mx-20 my-10'>
          <p className='text-4xl font-bold'>Login</p>
          <form onSubmit={formik.handleSubmit} className='flex flex-col gap-5'>
            <input
              className='px-5 py-3 outline-none bg-[#F0EDFF] rounded-xl focus:bg-[#d7d7d7c5]'
              placeholder='Username'
              type='text'
              name='username'
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.username}
            />
            {formik.touched.username && formik.errors.username ? (
              <div className='text-red-500 absolute bottom-71'>{formik.errors.username}</div>
            ) : null}

            <input
              className='px-5 py-3 mt-5 outline-none bg-[#F0EDFF] rounded-xl focus:bg-[#d7d7d7c5]'
              placeholder='Password'
              type='password'
              name='password'
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.password}
            />
            {formik.touched.password && formik.errors.password ? (
              <div className='text-red-500 absolute bottom-48'>{formik.errors.password}</div>
            ) : null}

            <button
              type='submit'
              className='bg-gradient-to-r mt-5 from-[#85F481] to-[#05914E] hover:from-[#05914E] hover:to-[#85F481] cursor-pointer px-10 py-4 rounded-xl w-fit text-white font-bold m-auto'
            >
              Login
            </button>
          </form>
        </div>
      </section>
      <section className="bg-[url('/bgImage.png')] h-[100vh] w-1/2 bg-cover bg-center flex items-center flex-col pt-15 gap-8">
        <p className='text-white text-4xl font-bold'>New to </p>
        <p className='text-white text-[90px] font-bold'>SPENTRA?</p>
        <div>
          <p className='text-white text-xl text-center'>Sign up today and take control of your financial journey.</p>
          <p className='text-white text-2xl text-center'>Start tracking your expenses and unlock new possibilities</p>
        </div>
        <div className='flex justify-center flex-col gap-5'>
          <hr className='w-130 text-white' />
          <NavLink 
          to='/signup'
          className='cursor-pointer bg-white text-black px-10 py-4 rounded-xl w-fit text-xl m-auto'>Sign up</NavLink>
          
        </div>
      </section>
    </div>
  );
};

export default Login;