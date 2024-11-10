// Hàm cập nhật giao diện với lịch sử trò chuyện
function updateChatHistory(history) {
    const historyList = $('#historyList');
    historyList.empty(); // Xóa nội dung cũ
    history.forEach(item => {
        historyList.append(`<div class="user-message">${item.user}</div>`);
        historyList.append(`<div class="assistant-message">${item.assistant}</div>`);
    });
}

$(document).ready(function() {
    // Xử lý khi gửi văn bản
    $('#inputForm').on('submit', function(event) {
        event.preventDefault();
        let userInput = $('#inputField').val();

        $.ajax({
            url: '/process',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'input': userInput }),
            success: function(response) {
                $('#responseText').text(response.response);  // Hiển thị phản hồi của AI
                updateChatHistory(response.history);  // Cập nhật lịch sử
            },
            error: function() {
                $('#responseText').text('Error: Unable to get response.');
            }
        });
    });

    // Xử lý khi nhấn nút Record
    $('#recordButton').on('click', function() {
        $.ajax({
            url: '/record',
            type: 'POST',
            success: function(response) {
                $('#responseText').text(response.response);  // Hiển thị phản hồi của AI sau khi ghi âm
                updateChatHistory(response.history);  // Cập nhật lịch sử
            },
            error: function() {
                $('#responseText').text('Error: Unable to process the recording.');
            }
        });
    });
});
