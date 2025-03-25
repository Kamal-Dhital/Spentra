import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { NavLink, useNavigate } from 'react-router-dom';

const Signup = () => {
  const formik = useFormik({
    initialValues: {
      fullName: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validationSchema: Yup.object({
      fullName: Yup.string()
        .min(3, 'Full name must be at least 3 characters')
        .required('Full name is required'),
      email: Yup.string()
        .email('Invalid email address')
        .required('Email is required'),
      password: Yup.string()
        .min(8, 'Password must be at least 8 characters')
        .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
        .required('Password is required'),
      confirmPassword: Yup.string()
        .oneOf([Yup.ref('password'), null], 'Passwords must match')
        .required('Confirm password is required'),
    }),
    onSubmit: (values) => {
      console.log('Form Data:', values);
    },
  });

  return (
    <div className='flex'>

      {/* Left Section */}
      <section className="bg-[url('/bgImage.png')] h-[100vh] w-1/2 bg-cover bg-center flex items-center justify-center   flex-col pt-15 gap-8">
       <img 
       className='w-90'
       src="wallet.png" alt="" />
       <div className='flex flex-col gap-3'>
        {/* Redirect to Login */}
       <p className='text-center mt-5 uppercase text-xl font-bold text-[#fff]'>
            Already have an account? 

          </p>
          <NavLink 
                    to='/login'
                    className='cursor-pointer bg-white text-black px-10 py-2 rounded-xl w-fit text-xl m-auto'>Login</NavLink>
       </div>
       
      </section>

      {/* Right Section */}
      <section className='flex flex-col w-1/2'>
        <div className='flex justify-center items-center'>
          <img className='w-35' src='logo.png' alt='Logo' />
        </div>

        <div className='flex flex-col gap-5 mx-20 my-10'>
          <p className='text-2xl uppercase mt-[-20px] font-bold'>Sign up</p>
          <form onSubmit={formik.handleSubmit} className='flex flex-col gap-5 ml-10 '>

            {/* Full Name Input */}
            <input
              className='px-5 py-3 outline-none bg-[#F0EDFF] rounded-xl focus:bg-[#d7d7d7c5]'
              placeholder='Full Name'
              type='text'
              name='fullName'
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.fullName}
            />
            {formik.touched.fullName && formik.errors.fullName ? (
              <div className='text-red-500 absolute top-62 ml-3'>{formik.errors.fullName}</div>
            ) : null}

            {/* Email Input */}
            <input
              className='px-5 py-3 outline-none bg-[#F0EDFF] rounded-xl focus:bg-[#d7d7d7c5]'
              placeholder='Email'
              type='email'
              name='email'
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.email}
            />
            {formik.touched.email && formik.errors.email ? (
              <div className='text-red-500 absolute top-79 ml-3'>{formik.errors.email}</div>
            ) : null}

            {/* Password Input */}
            <input
              className='px-5 py-3 outline-none bg-[#F0EDFF] rounded-xl focus:bg-[#d7d7d7c5]'
              placeholder='Password'
              type='password'
              name='password'
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.password}
            />
            {formik.touched.password && formik.errors.password ? (
              <div className='text-red-500 absolute top-96 ml-3'>{formik.errors.password}</div>
            ) : null}

            {/* Confirm Password Input */}
            <input
              className='px-5 py-3 outline-none bg-[#F0EDFF] rounded-xl focus:bg-[#d7d7d7c5]'
              placeholder='Confirm Password'
              type='password'
              name='confirmPassword'
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.confirmPassword}
            />
            {formik.touched.confirmPassword && formik.errors.confirmPassword ? (
              <div className='text-red-500 absolute top-113 ml-3'>{formik.errors.confirmPassword}</div>
            ) : null}

            <div className='flex gap-3'>
            <input
            className='w-4'
            type="checkbox" />
            <p className='text-sm'>I agree to Spentra’s <span className='font-bold'>Terms of Use</span> and <span className='font-bold'>Privacy Policy</span></p>
            </div>
            <hr className='w-100 text-[#c4b4b4]'/>
            {/* Signup Button */}
            <button
              type='submit'
              className='bg-gradient-to-r mt-5 from-[#85F481] to-[#05914E] hover:from-[#05914E] hover:to-[#85F481] cursor-pointer px-10 py-2 rounded-xl w-fit text-white font-bold m-auto'
            >
              Signup
            </button>
          </form>

         
        </div>
      </section>
    </div>
  );
};

export default Signup;
