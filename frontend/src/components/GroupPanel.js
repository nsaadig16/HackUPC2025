import React from 'react';
import Card from './Card';

const GroupPanel = ({ grupos }) => {
    const cardsPerRow = 2;
    const rows = [];

    for (let i = 0; i < grupos.length; i += cardsPerRow) {
        const row = grupos.slice(i, i + cardsPerRow);
        rows.push(row);
    }

    return (
        <div className='Pare'>
            {rows.map((row, rowIndex) => (
                <div key={rowIndex} className='flex flex-row justify-around items-center'> {/* Cambiado justify-center a justify-around */}
                    {row.map((grupo, index) => (
                        <div key={`${rowIndex}-${index}`} className='w-1/2 p-4'> {/* Añadido contenedor con ancho */}
                            <Card
                                Nom={grupo.Nom}
                                Destins={grupo.Destins}
                                Interessos={grupo.Interessos}
                            />
                        </div>
                    ))}
                    {/* Este div vacío causaba problemas de centrado en filas impares */}
                    {row.length === 1 && <div className='w-1/2 p-4 invisible' />} {/* Lo hacemos invisible para ocupar espacio sin mostrar nada */}
                </div>
            ))}
        </div>
    );
};

export default GroupPanel;