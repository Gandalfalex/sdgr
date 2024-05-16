import {useEffect} from 'react';
import {useLocation} from 'react-router-dom';

export const ExternalRedirect = () => {
    const location = useLocation();

    useEffect(() => {
        if (location.pathname === '/docs') {
            window.location.href = '/documentation';
        }
    }, [location.pathname]);

    return null;
};

