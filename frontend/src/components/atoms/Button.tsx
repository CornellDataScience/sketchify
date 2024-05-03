import { ReactNode } from "react";

type ButtonProps = {
  children: ReactNode;
  disabled?: boolean;
  [key: string]: any;
};

const Button = ({ children, disabled = false, ...props }: ButtonProps) => {
  if (disabled) {
    return (
      <button
        type="button"
        className="text-white bg-blue-400 dark:bg-blue-500 cursor-not-allowed font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"
        {...props}
      >
        {children}
      </button>
    );
  }
  return (
    <button
      type="button"
      className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
