// import { useAuthStore } from '@/stores';
import axios from "axios";
import { useAppStore } from "@/stores/app";

export const axiosWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE')
};

function request(method) {
    return async(url, body,contentType='application/json') => {
        const requestOptions = {
            method,
            // headers: authHeader(url)
            headers: {}
        };
        requestOptions.headers['Accept-Language']= useAppStore().language
        console.log(requestOptions.headers['Accept-Language'])
        if (body) {
            requestOptions.headers['Content-Type'] = contentType;
            if(contentType=='application/json')requestOptions.body = JSON.stringify(body);
            if(contentType=='multipart/form-data') requestOptions.body = body;
        }

        try{
           console.log({method, url, headers:requestOptions.headers, data:requestOptions.body})
            const response= await axios({method, url, headers:requestOptions.headers, data:requestOptions.body})
            return handleResponse(response)
        }catch(e){
            return handleResponse(e.response) || e
        }
        
         
    }
}

// helper functions

// function authHeader(url) {
//     // return auth header with jwt if user is logged in and request is to the api url
//     const { user } = useAuthStore();
//     const isLoggedIn = !!user?.token;
//     const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL);
//     if (isLoggedIn && isApiUrl) {
//         return { Authorization: `Bearer ${user.token}` };
//     } else {
//         return {};
//     }
    
// }

function handleResponse(response) {

    const status= response.status
    const error = (response.data && response.data.message) || response.statusText;
    switch(status){

        case 403:
        case 401:
            //   const { user, logout } = useAuthStore(); 
            //   if (user) logout();
            return Promise.reject(error)
        case 500:
            return Promise.reject(error)
        case 200:
            return response
        default:
            return Promise.reject(error)
    }

}