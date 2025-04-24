// Simulação de fetch de dados
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/network-status')
    .then(res => res.json())
    .then(data => {
      document.getElementById('bandwidth').textContent = data.bandwidth;
      document.getElementById('network-stability').textContent = data.stable ? 'Sim' : 'Não';

      const deviceList = document.getElementById('device-list');
      data.devices.forEach(device => {
        const li = document.createElement('li');
        li.textContent = `${device.name} (${device.ip})`;
        deviceList.appendChild(li);
      });

      document.getElementById('router-info').textContent = data.router.model;
      document.getElementById('switch-info').textContent = `${data.switch.model} (${data.switch.ports} portas)`;
    });
});
