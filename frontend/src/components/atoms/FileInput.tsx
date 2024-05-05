import { ReactNode } from "react";

type FileInputProps = {
  [key: string]: any;
};

const FileInput = ({ children, ...props }: FileInputProps) => {
  return (
    <input
      className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
      type="file"
      {...props}
    />
  );
};

export default FileInput;
